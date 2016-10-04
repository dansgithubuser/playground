//
// MainPage.xaml.h
// Declaration of the MainPage class.
//

#pragma once

#include "MainPage.g.h"

namespace App1
{
	/// <summary>
	/// An empty page that can be used on its own or navigated to within a Frame.
	/// </summary>
	public ref class MainPage sealed
	{
	public:
		MainPage();
	private:
		typedef Windows::Devices::Bluetooth::Advertisement::BluetoothLEAdvertisementWatcher Watcher;
		typedef Windows::Devices::Bluetooth::Advertisement::BluetoothLEAdvertisementReceivedEventArgs Args;
		typedef Windows::Devices::Bluetooth::BluetoothLEDevice Device;
		void handleAdvertisement(Watcher^, Args^);
		Watcher^ _watcher;
		std::atomic<bool> _devicing=false;
		std::thread _thread;
	};
}
