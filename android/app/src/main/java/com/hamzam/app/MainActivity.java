package com.hamzam.app;
import android.app.*;import android.os.*;import android.webkit.*;import android.view.*;
public class MainActivity extends Activity{public void onCreate(Bundle b){super.onCreate(b);WebView w=new WebView(this);w.getSettings().setJavaScriptEnabled(true);w.getSettings().setDomStorageEnabled(true);w.setWebViewClient(new WebViewClient());w.loadUrl(BuildConfig.HAMZAM_URL);setContentView(w);}}
