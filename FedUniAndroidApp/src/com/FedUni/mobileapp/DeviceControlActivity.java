package com.FedUni.mobileapp;

import org.alexd.jsonrpc.JSONRPCClient;
import org.alexd.jsonrpc.JSONRPCParams;

import android.os.AsyncTask;
import android.os.Bundle;
import android.app.Activity;
import android.content.Intent;
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

		class getMonitorStatusOp extends AsyncTask<Void, Void, Boolean> {
			@Override
			protected Boolean doInBackground(Void... params) {
				// Create client specifying JSON-RPC version 2.0
				JSONRPCClient client = JSONRPCClient.create("http://"
						+ MainActivity.RaspberryPiAddress.getAddress()
								.getHostAddress() + ":"
						+ MainActivity.RaspberryPiAddress.getPort(),
						JSONRPCParams.Versions.VERSION_2);

				client.setConnectionTimeout(2000);
				client.setSoTimeout(2000);

				try {
					return client.callBoolean("get_monitor_state");
				} catch (Exception e) {
					e.printStackTrace();
				}

				// and finally return the result
				return false;
			}

			@Override
			protected void onPostExecute(Boolean result) {
			}

			@Override
			protected void onPreExecute() {
			}

			@Override
			protected void onProgressUpdate(Void... values) {
			}
		}

		try {
			return new getMonitorStatusOp().execute().get();
		} catch (Exception e) {
			return false;
		}
	}

	// Instructs the monitor to change it's monitoring status
	private void toggleMonitorStatus() {
		class setMonitorStatusOp extends AsyncTask<Boolean, Void, Void> {
			@Override
			protected Void doInBackground(Boolean... params) {
				// Create client specifying JSON-RPC version 2.0
				JSONRPCClient client = JSONRPCClient.create("http://"
						+ MainActivity.RaspberryPiAddress.getAddress()
								.getHostAddress() + ":"
						+ MainActivity.RaspberryPiAddress.getPort(),
						JSONRPCParams.Versions.VERSION_2);

				client.setConnectionTimeout(2000);
				client.setSoTimeout(2000);

				try {
					client.callBoolean("set_monitor_state", params[0]);
				} catch (Exception e) {
					e.printStackTrace();
				}

				return null;
			}

			@Override
			protected void onPostExecute(Void result) {
			}

			@Override
			protected void onPreExecute() {
			}

			@Override
			protected void onProgressUpdate(Void... values) {
			}
		}

		try {
			new setMonitorStatusOp().execute(!bCurrentMonitorState).get();
		} catch (Exception e) {
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
	
	// Called when the Live Stream is clicked
	public void btnStream_onClick(View v) {
		// Only do anything if we have a monitor address
		if (MainActivity.bSuccessfullyConnected) {
			// Change to the stream activity
			Intent intent = new Intent(v.getContext(), LiveStream.class);
			startActivity(intent);
		}
	}

}
