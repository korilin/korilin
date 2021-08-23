package com.korilin.app

import android.app.Activity
import android.content.Intent
import android.os.Handler
import android.os.Looper
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.RecyclerView

class SourceResearch : AppCompatActivity() {

    lateinit var textView: TextView

    fun findView() {
        textView.text = "Hello"
    }

    fun recyclerView() {
        RecyclerView(Application.context)
    }

    fun activityThread(){
        Activity()
    }

    fun handler() {
        Handler(Looper.getMainLooper()!!)
    }

    fun start(){
        startActivity(Intent())
    }
}