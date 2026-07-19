import org.jetbrains.kotlin.gradle.dsl.JvmTarget

plugins {
    alias(libs.plugins.androidApplication)
}

kotlin {
    compilerOptions {
        jvmTarget = JvmTarget.JVM_1_8
    }
}

android {
    namespace = "eu.kanade.tachiyomi.extension"
    compileSdk = 37

    defaultConfig {
        applicationId = "eu.kanade.tachiyomi.extension"
        applicationIdSuffix = "all.dummyextension"
        minSdk = 26
        targetSdk = 37
        versionCode = 21
        versionName = "${libs.versions.extlib.get().substringBeforeLast('.')}.$versionCode"
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
}

dependencies {
    compileOnly(libs.tachiyomi.lib)
    compileOnly(libs.okhttp)
    compileOnly(libs.coroutines)
}
