package com.korilin.app

import android.annotation.SuppressLint
import android.app.Application
import android.content.Context


const val PROTOCOL = "https://"
const val HOST = "korilin.com"
const val BASE_URL = "$PROTOCOL$HOST"
const val BLOG_URL = "$BASE_URL/blog"

class Application : Application() {

    companion object {
        @SuppressLint("StaticFieldLeak")
        lateinit var context: Context
    }

    override fun onCreate() {
        super.onCreate()
        context = applicationContext
    }
}