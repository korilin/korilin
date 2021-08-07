package com.korilin.app

import android.annotation.SuppressLint
import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.content.Intent
import android.graphics.Color
import android.net.Uri
import android.os.Build
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.view.KeyEvent
import android.view.View
import android.webkit.WebResourceRequest
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.Toast
import androidx.core.view.ViewCompat
import com.google.android.material.floatingactionbutton.FloatingActionButton
import com.korilin.app.databinding.ActivityMainBinding

class MainActivity : AppCompatActivity() {

    private lateinit var mainBinding: ActivityMainBinding
    private lateinit var webView: WebView

    private var optionIn = false

    private lateinit var clipboardManager: ClipboardManager

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        mainBinding = ActivityMainBinding.inflate(layoutInflater)

        webView = mainBinding.webview.apply {
            loadUrl(BLOG_URL)
            settings.javaScriptEnabled = true
            setBackgroundColor(Color.WHITE)
            webViewClient = object : WebViewClient() {
                override fun shouldOverrideUrlLoading(view: WebView?, request: WebResourceRequest): Boolean {
                    if (request.url?.host == HOST) return false
                    Intent(Intent.ACTION_VIEW, Uri.parse(request.url.toString())).apply {
                        startActivity(this)
                    }
                    return true
                }
            }
        }

        clipboardManager = getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager

        mainBinding.apply {

            copy.apply {
                hide()
                setOnClickListener {
                    clipboardManager.setPrimaryClip(
                        ClipData.newPlainText("link", webView.url)
                    )
                    Toast.makeText(context, "链接已复制到剪切板", Toast.LENGTH_LONG).show()
                }
            }

            share.apply {
                hide()
                setOnClickListener {
                    Intent().apply {
                        action = Intent.ACTION_SEND
                        type = "text/plain"
                        putExtra(Intent.EXTRA_SUBJECT, "来自 Kori Lin 个人博客的链接")
                        putExtra(Intent.EXTRA_TEXT, "${webview.title} ：${webview.url}")
                    }.also {
                        Intent.createChooser(it, "分享")
                    }.apply {
                        startActivity(this)
                    }
                }
            }

            option.apply {
                show()
                setOnClickListener {
                    if (optionIn) {
                        setImageResource(android.R.drawable.ic_dialog_dialer)
                        copy.hide()
                        share.hide()
                    } else {
                        setImageResource(android.R.drawable.ic_menu_close_clear_cancel)
                        copy.show()
                        share.show()
                    }
                    optionIn = !optionIn
                }
            }
        }

        ViewCompat.getWindowInsetsController(mainBinding.root)

        window.apply {
            decorView.systemUiVisibility = View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN or View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR
            statusBarColor = Color.TRANSPARENT
        }

        setContentView(mainBinding.root)
    }

    override fun onKeyDown(keyCode: Int, event: KeyEvent?): Boolean {
        if (keyCode == KeyEvent.KEYCODE_BACK && webView.canGoBack()) {
            webView.goBack()
            return true
        }
        return super.onKeyDown(keyCode, event)
    }
}