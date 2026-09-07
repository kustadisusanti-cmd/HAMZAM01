package com.hamzam.ai;

import android.app.Activity;
import android.os.Bundle;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.*;

public class MainActivity extends Activity {
    EditText url; SharedPreferences prefs;
    @Override public void onCreate(Bundle b){ super.onCreate(b); setContentView(R.layout.activity_main);
        prefs=getSharedPreferences("hamzam",0); url=findViewById(R.id.url); TextView status=findViewById(R.id.status);
        url.setText(prefs.getString("url",""));
        findViewById(R.id.save).setOnClickListener(v->{ String u=url.getText().toString().trim(); if(!u.startsWith("https://")){status.setText("URL harus diawali https://"); return;} prefs.edit().putString("url",u).apply(); status.setText("URL HAMZAM tersimpan."); });
        findViewById(R.id.open).setOnClickListener(v->{ String u=url.getText().toString().trim(); if(u.isEmpty()){status.setText("Masukkan URL Web App HAMZAM terlebih dahulu.");return;} prefs.edit().putString("url",u).apply(); openWeb(u); });
    }
    void openWeb(String u){ WebView w=new WebView(this); setContentView(w); w.setBackgroundColor(Color.rgb(7,11,18)); WebSettings s=w.getSettings(); s.setJavaScriptEnabled(true); s.setDomStorageEnabled(true); s.setAllowFileAccess(true); s.setAllowContentAccess(true); s.setBuiltInZoomControls(false); s.setDisplayZoomControls(false); w.setWebViewClient(new WebViewClient()); w.setWebChromeClient(new WebChromeClient()); w.loadUrl(u); }
    @Override public void onBackPressed(){ setContentView(R.layout.activity_main); onCreate(null); }
}
