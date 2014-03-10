package com.FedUni.mobileapp;

import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.net.NetworkInterface;
import java.net.Socket;
import java.net.SocketAddress;
import java.util.Collections;
import java.util.List;

import org.apache.http.conn.util.InetAddressUtils;

import android.os.Bundle;
import android.os.Handler;
import android.app.Activity;
import android.content.Intent;
import android.view.Menu;
import android.widget.ProgressBar;

public class MainActivity extends Activity {

	// The device count used
	int nCurDevice;
	// Maximum device count
	int nMaxDevice = 256;

	// Set to true when the monitor device is found
	public static boolean bSuccessfullyConnected;
	// If a device is found, this has the IP info
	public static SocketAddress RaspberryPiAddress;

	/**
	 * Get IP address from first non-localhost interface
	 * 
	 * @param ipv4
	 *            true=return ipv4, false=return ipv6
	 * @return address or empty string
	 */

	// TODO: Rewrite - This is code taken from the internet
	public static String getIPAddress(boolean useIPv4) {
		try {
			List<NetworkInterface> interfaces = Collections
					.list(NetworkInterface.getNetworkInterfaces());
			for (NetworkInterface intf : interfaces) {
				List<InetAddress> addrs = Collections.list(intf
						.getInetAddresses());
				for (InetAddress addr : addrs) {
					if (!addr.isLoopbackAddress()) {
						String sAddr = addr.getHostAddress().toUpperCase();
						boolean isIPv4 = InetAddressUtils.isIPv4Address(sAddr);
						if (useIPv4) {
							if (isIPv4)
								return sAddr;
						} else {
							if (!isIPv4) {
								int delim = sAddr.indexOf('%'); // drop ip6 port
																// suffix
								return delim < 0 ? sAddr : sAddr.substring(0,
										delim);
							}
						}
					}
				}
			}
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
	protected void startRaspberryPiSearch() {

		// Fire off a thread to do some work that we shouldn't do directly in
		// the UI thread
		Thread t = new Thread() {
			@Override
			public void run() {

				// Get our local address
				String LocalAddr = getIPAddress(true);

				// Extract the subnet (Not really a subnet, it fetches the IP up
				// to
				// the last decimal point.
				String LocalAddrSubnet = LocalAddr.substring(0,
						LocalAddr.lastIndexOf('.'));

				// Try connecting to each address on the network
				while (nCurDevice < nMaxDevice) {

					// Create the IP address
					String TestLocalAddr = LocalAddrSubnet + "."
							+ Integer.toString(nCurDevice);

					// Create a socket
					Socket s = new Socket();
					InetSocketAddress remoteAddr = new InetSocketAddress(
							TestLocalAddr, 3487);

					try {
						// To to connect the socket
						s.connect(remoteAddr, 250);
						if (s.isConnected()) {
							// Woo we connected :D
							bSuccessfullyConnected = true;
							s.close();
							RaspberryPiAddress = new InetSocketAddress(
									TestLocalAddr, 3487);

							mHandler.post(mUpdateResults);

							return;
						}
					} catch (Exception e) {
					}

					// Oh... No device here, better keep searching
					nCurDevice++;
					mHandler.post(mUpdateResults);
				}
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

		// Update the progress bar
		ProgressBar pBar = (ProgressBar) findViewById(R.id.searchProgress);
		pBar.setProgress(nCurDevice);
	}

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);

		// Set global vars
		nCurDevice = 0;
		bSuccessfullyConnected = false;

		// Set up the progress bar
		ProgressBar pBar = (ProgressBar) findViewById(R.id.searchProgress);
		pBar.setMax(nMaxDevice);

		// Start searching for the device
		startRaspberryPiSearch();
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.main, menu);
		return true;
	}

}
