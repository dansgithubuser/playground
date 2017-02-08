#include <bluetooth/bluetooth.h>//hci_lib.h depends on this, htobs
#include <bluetooth/hci.h>//hci_lib.h depends on this
#include <bluetooth/hci_lib.h>

#include <unistd.h>//for close

#include <iomanip>
#include <sstream>
#include <stdexcept>
#include <vector>

namespace bluez{

struct DeviceId{ int i; };
struct DeviceDescriptor{ int i; };
struct Advertisement{
	std::vector<uint8_t> address;
	std::vector<uint8_t> data;
};

std::string toString(uint8_t b){
	std::stringstream ss;
	ss<<std::hex<<std::setw(2)<<std::setfill('0')<<(int)b;
	return ss.str();
}

std::string toString(const uint8_t* b, unsigned size){
	std::stringstream ss;
	for(unsigned i=0; i<size; ++i){
		ss<<toString(b[i]);
		if(i!=size-1) ss<<' ';
	}
	return ss.str();
}

std::string toString(const std::vector<uint8_t>& v){
	return toString(v.data(), v.size());
}

std::string toString(const Advertisement& a){
	return toString(a.address)+" - "+toString(a.data);
}

DeviceId find(){
	int deviceId=hci_get_route(NULL/*first device*/);
	if(deviceId<0) throw std::runtime_error("error finding device");
	return DeviceId{deviceId};
}

DeviceDescriptor open(DeviceId deviceId){
	int deviceDescriptor=hci_open_dev(deviceId.i);
	if(deviceDescriptor<0) throw std::runtime_error("error opening device");
	return DeviceDescriptor{deviceDescriptor};
}

void setScanParameters(DeviceDescriptor deviceDescriptor, int interval, int window){
	hci_le_set_scan_enable(deviceDescriptor.i, 0, 0, 1000);
	if(hci_le_set_scan_parameters(deviceDescriptor.i,
		1,//active, 0 for passive
		htobs(interval), htobs(window),
		LE_PUBLIC_ADDRESS,//address type of self
		0,//don't do whitelist filtering
		0//no timeout
	)<0) throw std::runtime_error("error setting scan parameters");
}

void toggleScan(DeviceDescriptor deviceDescriptor, bool enable){
	if(hci_le_set_scan_enable(deviceDescriptor.i, enable?1:0,
		0,//no duplicate filtering
		0//no timeout
	)<0) throw std::runtime_error("error toggling scan");
}

Advertisement inquire(DeviceDescriptor deviceDescriptor){
	struct hci_filter f;
	hci_filter_clear(&f);
	hci_filter_set_ptype(HCI_EVENT_PKT, &f);
	hci_filter_set_event(EVT_LE_META_EVENT, &f);
	if(setsockopt(deviceDescriptor.i, SOL_HCI, HCI_FILTER, &f, sizeof f)<0) throw std::runtime_error("error setting socket options "+std::to_string(errno));
	uint8_t buffer[HCI_MAX_EVENT_SIZE];
	int r=read(deviceDescriptor.i, buffer, sizeof buffer);
	if(r<0) throw std::runtime_error("error reading socket");
	evt_le_meta_event* meta=(evt_le_meta_event*)(buffer+1+HCI_EVENT_HDR_SIZE);
	if(meta->subevent!=EVT_LE_ADVERTISING_REPORT) throw std::runtime_error("error: unexpected subevent type");
	le_advertising_info* info=(le_advertising_info*)(meta->data+1);
	Advertisement result;
	result.address.assign(info->bdaddr.b, info->bdaddr.b+6);
	result.data.assign(info->data, info->data+info->length);
	return result;
}

int close(DeviceDescriptor deviceDescriptor){
	return ::close(deviceDescriptor.i);
}

}//namespace bluez
