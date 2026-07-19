// Top-level build file where you can add configuration options common to all sub-projects/modules.
plugins {
    alias(libs.plugins.androidApplication) apply false
}

buildscript {
    dependencies {
        classpath(libs.gradle.agp)
        classpath(libs.gradle.kotlin)
    }
}
