using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Runtime.InteropServices.WindowsRuntime;
using Windows.Foundation;
using Windows.Foundation.Collections;
using Windows.UI.Xaml;
using Windows.UI.Xaml.Controls;
using Windows.UI.Xaml.Controls.Primitives;
using Windows.UI.Xaml.Data;
using Windows.UI.Xaml.Input;
using Windows.UI.Xaml.Media;
using Windows.UI.Xaml.Navigation;

using Windows.Devices.Bluetooth.Advertisement;
using System.Text;
using Windows.Storage.Streams;
using System.Diagnostics;
using Windows.Devices.Bluetooth;

// The Blank Page item template is documented at http://go.microsoft.com/fwlink/?LinkId=402352&clcid=0x409

namespace App1
{
    /// <summary>
    /// An empty page that can be used on its own or navigated to within a Frame.
    /// </summary>
    public sealed partial class MainPage : Page
    {
        private BluetoothLEAdvertisementWatcher _watcher;
        private bool _handlingAdvertisement = false;
        private bool _devicing = false;

        public MainPage()
        {
            this.InitializeComponent();
            _watcher = new BluetoothLEAdvertisementWatcher();
            _watcher.Received += handleAdvertisement;
            _watcher.Start();
        }

        private string bufferToString(IBuffer buffer)
        {
            byte[] bytes;
            using (var reader = DataReader.FromBuffer(buffer))
            {
                bytes = new byte[buffer.Length];
                reader.ReadBytes(bytes);
            }
            return BitConverter.ToString(bytes);
        }

        private async void handleAdvertisement(BluetoothLEAdvertisementWatcher watcher, BluetoothLEAdvertisementReceivedEventArgs eventArgs)
        {
            if (_handlingAdvertisement) Debug.WriteLine("wtf");
            _handlingAdvertisement = true;
            StringBuilder sb = new StringBuilder();
            sb.Append(eventArgs.RawSignalStrengthInDBm.ToString());
            sb.Append(" ");
            sb.Append(eventArgs.AdvertisementType.ToString());
            sb.Append("\n\t");
            var sections = eventArgs.Advertisement.DataSections;
            for (int i = 0; i < sections.Count; ++i)
            {
                sb.Append(sections[i].DataType.ToString("X2"));
                sb.Append(": ");
                sb.Append(bufferToString(sections[i].Data).Replace("-", " "));
                sb.Append("  ");
            }
            Debug.WriteLine(sb.ToString());
            _handlingAdvertisement = false;
            if (_devicing) return;
            _devicing = true;
            var wantExceptions = true;
            wantExceptions = false;//comment to get exceptions!
            if(wantExceptions){
                BluetoothLEDevice device = await BluetoothLEDevice.FromBluetoothAddressAsync(eventArgs.BluetoothAddress);
                Debug.WriteLine("created device");
                var service = device.GetGattService(new Guid("1800"));
                if (service == null)
                {
                    _devicing = false;
                    return;
                }
                var characteristics = service.GetCharacteristics(new Guid("2a00"));
                if (characteristics == null)
                {
                    _devicing = false;
                    return;
                }
                Debug.WriteLine("got characteristic");
                foreach (var characteristic in characteristics)
                {
                    var value = await characteristic.ReadValueAsync();
                    Debug.WriteLine("got device name:");
                    Debug.WriteLine(bufferToString(value.Value));
                }
            }
            _devicing = false;
        }
    }
}
