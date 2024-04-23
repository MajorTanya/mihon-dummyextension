plugins {
    alias(libs.plugins.androidApplication)
    alias(libs.plugins.kotlinAndroid)
}

android {
    namespace = "eu.kanade.tachiyomi.extension"
    compileSdk = 34

    defaultConfig {
        applicationId = "eu.kanade.tachiyomi.extension"
        applicationIdSuffix = "all.dummyextension"
        minSdk = 26
        targetSdk = 34
        versionCode = 16
        versionName = "1.4.$versionCode"
        base {
            archivesName = "tachiyomi-$applicationIdSuffix-v$versionName"
        }
    }

    signingConfigs {
        create("release") {
            storeFile = rootProject.file("signingkey.jks")
            storePassword = System.getenv("KEY_STORE_PASSWORD")
            keyAlias = System.getenv("ALIAS")
            keyPassword = System.getenv("KEY_PASSWORD")
        }
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro",
            )
            signingConfig = signingConfigs.getByName("release")
        }
    }

    dependenciesInfo {
        includeInApk = false
    }

    buildFeatures {
        resValues = false
        shaders = false
        buildConfig = true
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_1_8
        targetCompatibility = JavaVersion.VERSION_1_8
    }

    kotlinOptions {
        jvmTarget = JavaVersion.VERSION_1_8.toString()
    }
}

dependencies {
    compileOnly(libs.tachiyomi.lib)
    compileOnly(libs.okhttp)
}
