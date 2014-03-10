package com.FedUni.mobileapp;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.Socket;

import android.os.AsyncTask;
import android.os.Bundle;
import android.app.Activity;
import android.view.Menu;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

public class DeviceControlActivity extends Activity {

	// Global variable to keep track of the monitoring status
	private boolean bCurrentMonitorState;

	// This function launches a request to the monitor to fetch it's current
	// monitoring status
	private boolean getMonitorStatus() {
		// Thread extension class used to return the result
		class GetMonitorStatusThread extends Thread {
			public boolean result = false;

			public void run() {
				// create a socket
				Socket s = new Socket();
				try {
					// connect it
					s.connect(MainActivity.RaspberryPiAddress);
					DataInputStream dataInputStream = new DataInputStream(
							s.getInputStream());
					DataOutputStream dataOutputStream = new DataOutputStream(
							s.getOutputStream());

					// 0x00 is used to fetch the current monitor status
					dataOutputStream.writeByte(0);

					// read the result
					if (dataInputStream.readByte() == 0)
						result = false;
					else
						result = true;

					// clean up the socket
					s.close();
				} catch (Exception e) {
					// clean up the socket
					try {
						s.close();
					} catch (Exception e1) {
					}
				}
			}
		}

		// Create a class instance
		GetMonitorStatusThread t = new GetMonitorStatusThread();
		// and start it
		t.start();
		// and wait for it to finish
		try {
			t.join();
		} catch (InterruptedException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}

		// and finally return the result
		return t.result;
	}

	// Instructs the monitor to change it's monitoring status
	private void toggleMonitorStatus() {
		// Thread extension used to send info to the monitor
		class ToggleMonitorStatusThread extends Thread {
			public void run() {
				// create the socket
				Socket s = new Socket();
				try {
					// connect to the monitor
					s.connect(MainActivity.RaspberryPiAddress);
					DataOutputStream dataOutputStream = new DataOutputStream(
							s.getOutputStream());

					// tell the monitor we are about to give it a new state
					dataOutputStream.writeByte(1);

					// send the new state
					if (bCurrentMonitorState)
						dataOutputStream.writeByte(0);
					else
						dataOutputStream.writeByte(1);

					// clean up the socket
					s.close();
				} catch (Exception e) {
					// cleanup the socket
					try {
						s.close();
					} catch (Exception e1) {
					}
				}
			}
		}

		// create the thread
		ToggleMonitorStatusThread t = new ToggleMonitorStatusThread();
		// and start it
		t.start();
		// and wait for it to finish
		try {
			t.join();
		} catch (InterruptedException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
	}

	// utility function for changing the toggle button text
	public void updateMonitorButtonStatus() {
		// only need to do this if we have a valid monitor
		if (MainActivity.bSuccessfullyConnected) {
			// now fetch the monitoring state and set the toggle button caption
			String status = "Start Monitoring";

			bCurrentMonitorState = getMonitorStatus();
			if (bCurrentMonitorState) {
				status = "Stop Monitoring";
			}

			Button bt = (Button) findViewById(R.id.btnToggleMonitoring);
			bt.setText(status);
		}
	}

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_device_control);

		// Get the text view
		TextView tv = (TextView) findViewById(R.id.textDeviceFound);
		// update it with the address of the monitor
		tv.setText("Monitor located at: "
				+ MainActivity.RaspberryPiAddress.toString());
		
		// Set the toggle button caption
		updateMonitorButtonStatus();
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.device_control, menu);
		return true;
	}

	// Called when the toggle button is clicked
	public void btnToggleMonitoring_onClick(View v) {
		// Only do anything if we have a monitor address
		if (MainActivity.bSuccessfullyConnected) {
			// update the monitor status
			toggleMonitorStatus();
			// and fetch the new state to make sure the change was successful 
			updateMonitorButtonStatus();
		}
	}

}
