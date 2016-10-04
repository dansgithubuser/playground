//
// MainPage.xaml.cpp
// Implementation of the MainPage class.
//

#include "pch.h"
#include "MainPage.xaml.h"

#include <iomanip>
#include <sstream>

using namespace App1;

using namespace Platform;
using namespace Windows::Foundation;
using namespace Windows::Foundation::Collections;
using namespace Windows::UI::Xaml;
using namespace Windows::UI::Xaml::Controls;
using namespace Windows::UI::Xaml::Controls::Primitives;
using namespace Windows::UI::Xaml::Data;
using namespace Windows::UI::Xaml::Input;
using namespace Windows::UI::Xaml::Media;
using namespace Windows::UI::Xaml::Navigation;

// The Blank Page item template is documented at http://go.microsoft.com/fwlink/?LinkId=402352&clcid=0x409

MainPage::MainPage()
{
	InitializeComponent();
	_watcher=ref new Watcher;
	using Windows::Foundation::TypedEventHandler;
	/*How to figure this junk by reading MSDN
	MSDN says that watcher.Received is:
		public:
		event TypedEventHandler<BluetoothLEAdvertisementWatcher, BluetoothLEAdvertisementReceivedEventArgs>^ Received {
		  Windows::Foundation::EventRegistrationToken add(TypedEventHandler<BluetoothLEAdvertisementWatcher, BluetoothLEAdvertisementReceivedEventArgs>^ value);
		  void remove(Windows::Foundation::EventRegistrationToken token);
		}
	Which seems to boil down to:
		...
		event TypedEventHandler<ObjectType, ArgsType>^ EventMember
		...
	For which you can write the following code:
		class Class{
			Class(){
				...
				object.EventMember+=ref new TypedEventHandler<ObjectType^, ArgsType^>(this, &Class::handle);
			}
			handle(ObjectType^, ArgsType^){
				...
			}
		}
	*/
	_watcher->Received+=ref new TypedEventHandler<Watcher^, Args^>(this, &MainPage::handleAdvertisement);
	_watcher->Start();//make sure you have permission, or this will throw an exception, which doesn't end the app
}

static std::vector<uint8_t> bufferToStdVector(Windows::Storage::Streams::IBuffer^ buffer){
	auto reader=Windows::Storage::Streams::DataReader::FromBuffer(buffer);
	std::vector<uint8_t> v(reader->UnconsumedBufferLength);
	reader->ReadBytes(Platform::ArrayReference<uint8_t>(v.data(), v.size()));
	return v;
}

static void log(const std::string& s){
	OutputDebugStringA(s.c_str());
	OutputDebugStringA("\n");
}

static void log(const std::stringstream& ss){
	log(ss.str());
}

void MainPage::handleAdvertisement(Watcher^ watcher, Args^ args){
	std::stringstream ss;
	ss<<std::hex<<args->BluetoothAddress<<" "<<std::dec<<args->RawSignalStrengthInDBm<<" ";
	ss<<std::vector<std::string>{
		"ConnectableUndirected",
		"ConnectableDirected",
		"ScannableUndirected",
		"NonConnectableUndirected",
		"ScanResponse",
	}.at((int)args->AdvertisementType);
	ss<<"\n\t";
	try{
		if(!args->Advertisement->DataSections){
			log("lol got a null reference data section for some reason!");
			return;
		}
	}
	catch(Platform::NullReferenceException^ e){
		log("lol got a null reference for some reason!");
		return;
	}
	for(unsigned i=0; i<args->Advertisement->DataSections->Size; ++i){
		auto d=args->Advertisement->DataSections->GetAt(i);
		ss<<std::hex<<(unsigned)d->DataType<<": ";
		auto v=bufferToStdVector(d->Data);
		for(unsigned j=0; j<v.size(); ++j) ss<<std::hex<<std::setw(2)<<std::setfill('0')<<(unsigned)v[j]<<" ";
		ss<<" ";
	}
	log(ss);
	return;//comment to get exceptions!
	if(_devicing) return;
	_devicing=true;
	_thread=std::thread([this, args](){
		log("creating device");
		//MSDN says that FromBluetoothAddressAsync returns IAsyncOperation<BluetoothLEDevice>^
		//lol wutev
		IAsyncOperation<Device^>^ op=Device::FromBluetoothAddressAsync(args->BluetoothAddress);
		Concurrency::task<Device^> task=Concurrency::create_task(op);
		Concurrency::task<void> task2=task.then([this](Device^ device){
			log("created device");
			auto service=device->GetGattService(Platform::Guid({0x18, 0x00}));
			auto characteristics=service->GetCharacteristics(Platform::Guid({0x2a, 0x00}));
			for(unsigned i=0; i<characteristics->Size; ++i){
				log("got characteristic");
				using Windows::Devices::Bluetooth::GenericAttributeProfile::GattReadResult;
				IAsyncOperation<GattReadResult^>^ op=characteristics->GetAt(i)->ReadValueAsync();
				Concurrency::task<GattReadResult^> task=Concurrency::create_task(op);
				task.then([this](GattReadResult^ result){
					auto v=bufferToStdVector(result->Value);
					std::stringstream ss;
					ss<<"got device name: ";
					for(unsigned i=0; i<v.size(); ++i) ss<<v[i];
					log(ss);
					_devicing=false;
				});
			}
		});
		task2.wait();
	});
}
