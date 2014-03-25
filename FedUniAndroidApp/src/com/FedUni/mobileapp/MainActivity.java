package com.FedUni.mobileapp;

import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.net.Socket;
import android.net.wifi.WifiManager;
import android.os.Bundle;
import android.os.Handler;
import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.view.Menu;
import android.widget.TextView;

public class MainActivity extends Activity {

	// Set to true when the monitor device is found
	public static boolean bSuccessfullyConnected;
	// If a device is found, this has the IP info
	public static InetSocketAddress RaspberryPiAddress;

	// Simple function to get the current wifi IP
	public String getIPAddress(Context c) {
		try {
			WifiManager mgr = (WifiManager) c
					.getSystemService(Context.WIFI_SERVICE);
			int ip = mgr.getConnectionInfo().getIpAddress();

			String ipString = String.format("%d.%d.%d.%d", (ip & 0xff),
					(ip >> 8 & 0xff), (ip >> 16 & 0xff), (ip >> 24 & 0xff));

			return ipString;
		} catch (Exception ex) {
		} // for now eat exceptions
		return "";
	}

	// Need handler for callbacks to the UI thread
	final Handler mHandler = new Handler();

	// Create runnable for posting
	final Runnable mUpdateResults = new Runnable() {
		@Override
		public void run() {
			updateResultsInUi();
		}
	};

	// This function spawns a thread that gets the IP address of the current
	// device
	// and then extracts the subnet and searches the network for the raspberry
	// pi
	// monitor
	protected void startRaspberryPiConnection() {

		// Fire off a thread to do some work that we shouldn't do directly in
		// the UI thread
		Thread t = new Thread() {
			@Override
			public void run() {

				// Get our local address
				String LocalAddr = getIPAddress(getApplicationContext());

				// Extract the subnet (Not really a subnet, it fetches the IP up
				// to
				// the last decimal point.
				String LocalAddrSubnet = LocalAddr.substring(0,
						LocalAddr.lastIndexOf('.'));

				InetAddress currentPingAddr;

				// Try connecting to address on the network
				try {
					// build the next IP address
					currentPingAddr = InetAddress.getByName(LocalAddrSubnet
							+ ".250");

					// Create a socket
					Socket s = new Socket();
					InetSocketAddress remoteAddr = new InetSocketAddress(
							currentPingAddr, 3487);

					try {
						// To to connect the socket
						s.connect(remoteAddr);
						if (s.isConnected()) {
							// Woo we connected :D
							bSuccessfullyConnected = true;
							s.close();
							RaspberryPiAddress = new InetSocketAddress(
									currentPingAddr, 3487);

							mHandler.post(mUpdateResults);

							return;
						}
					} catch (Exception e) {
						e.printStackTrace();
					}
				} catch (Exception e) {
				}
				
				mHandler.post(mUpdateResults);
			}

		};
		t.start();
	}

	private void updateResultsInUi() {
		// Called to run in the UI thread so we can update the progress bar
		if (bSuccessfullyConnected) {
			// If we connected successfully, then jump to the next activity
			Intent intent = new Intent(this, DeviceControlActivity.class);
			startActivity(intent);

			return;
		}
		
		TextView tv = (TextView) findViewById(R.id.textConnecting);
		tv.setText("Error: Could not connect to monitor...\n Is your wifi on?");
	}

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);

		// Set global vars
		bSuccessfullyConnected = false;

		// Start searching for the device
		startRaspberryPiConnection();
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.main, menu);
		return true;
	}

}
