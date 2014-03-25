package com.FedUni.mobileapp;

import org.alexd.jsonrpc.JSONRPCClient;
import org.alexd.jsonrpc.JSONRPCParams;

import android.os.Bundle;
import android.os.Handler;
import android.app.Activity;
import android.content.Intent;
import android.view.Menu;
import android.view.View;
import android.widget.TextView;

public class LiveStream extends Activity {

	String StreamData = "";
	Boolean bKillStream;
	
	// Need handler for callbacks to the UI thread
	final Handler mHandler = new Handler();

	// Create runnable for posting
	final Runnable mUpdateResults = new Runnable() {
		@Override
		public void run() {
			updateResultsInUi();
		}
	};

	// This function spawns a thread that fetches stream data from the raspi
	protected void startStreamConnection() {

		// Fire off a thread to do some work that we shouldn't do directly in
		// the UI thread
		Thread t = new Thread() {
			@Override
			public void run() {

				// Create client specifying JSON-RPC version 2.0
				JSONRPCClient client = JSONRPCClient.create("http://"
						+ MainActivity.RaspberryPiAddress.getAddress()
								.getHostAddress() + ":"
						+ MainActivity.RaspberryPiAddress.getPort(),
						JSONRPCParams.Versions.VERSION_2);

				client.setConnectionTimeout(2000);
				client.setSoTimeout(2000);
				
				while (!bKillStream)
				{
					try {
						String data = client.callString("get_monitor_data");
						StreamData = data;
					} catch (Exception e) {
						e.printStackTrace();
					}
					
					mHandler.post(mUpdateResults);
					
					try {
						Thread.sleep(1000);
					} catch (InterruptedException e) {
						// TODO Auto-generated catch block
						e.printStackTrace();
					}
				}
			}

		};
		t.start();
	}
	
	private void updateResultsInUi() {
		// Called to run in the UI thread so we can update the stream status
		
		// Format is as follows
	    // int num sensors , str sensor 1 kind, int num elems, str[num] headers, float[num] values, str sensor 2 kind ...
		
		// for example
		// "1,Accelerometer,5,Time Stamp,Sample Rate,X Acceleration,Y Acceleration,Z Acceleration,2337,10.25,1944,1052,1748,"
		// if the first digit was a 2, there would be another sensor appended again starting with a number indicating the
		// number of fields of data it is transmitting 
		
		String txt = "";
		
		String[] Parts = StreamData.split(",");
		int nDevices = Integer.parseInt(Parts[0]);
		int idx = 1;
		
		for (int i = 0; i < nDevices; i++)
		{
			txt += Parts[idx] + "\n";
			int nParams = Integer.parseInt(Parts[idx+1]);
			
			idx += 2;
			for (int p = 0; p < nParams; p++)
			{
				txt += Parts[idx + p] + ":\t" + Parts[idx + nParams + p] + "\n";
			}
			
			idx += nParams*2;
			
			txt += "\n";
		}
		
		TextView tv = (TextView) findViewById(R.id.txtStreamInfo);
		tv.setText(txt);
	}
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_live_stream);
		
		bKillStream = false;
		
		startStreamConnection();
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.live_stream, menu);
		return true;
	}
	
	// Called when the Live Stream is clicked
	public void btnBack_OnClick(View v) {
		bKillStream = true;
		// Only do anything if we have a monitor address
		if (MainActivity.bSuccessfullyConnected) {
			// Change to the stream activity
			Intent intent = new Intent(this, DeviceControlActivity.class);
			startActivity(intent);
		}
	}
}
