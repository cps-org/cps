{
  "Name": "sample",
  "Description": "Sample CPS",
  "License": "BSD",
  "Version": "1.2.0",
  "Compat-Version": "0.8.0",
  "Platform": {
    "Isa": "x86_64",
    "Kernel": "linux",
    "C-Runtime-Vendor": "gnu",
    "C-Runtime-Version": "2.20",
    "Jvm-Version": "1.6"
  },
  "Configurations": [ "Optimized", "Debug" ],
  "Default-Components": [ "sample" ],
  "Components": {
    "sample-core": {
      "Type": "interface",
      "Definitions": [ "SAMPLE" ],
      "Includes": [ "@prefix@/include" ]
    },
    "sample": {
      "Type": "interface",
      "Configurations": {
        "Shared": {
          "Requires": [ ":sample-shared" ]
        },
        "Static": {
          "Requires": [ ":sample-static" ]
        }
      }
    },
    "sample-shared": {
      "Type": "dylib",
      "Requires": [ ":sample-core" ],
      "Configurations": {
        "Optimized": {
          "Location": "@prefix@/lib64/libsample.so.1.2.0"
        },
        "Debug": {
          "Location": "@prefix@/lib64/libsample_d.so.1.2.0"
        }
      }
    },
    "sample-static": {
      "Type": "archive",
      "Definitions": [ "SAMPLE_STATIC" ],
      "Requires": [ ":sample-core" ],
      "Configurations": {
        "Optimized": {
          "Location": "@prefix@/lib64/libsample.a"
        },
        "Debug": {
          "Location": "@prefix@/lib64/libsample_d.a"
        }
      }
    },
    "sample-tool": {
      "Type": "exe",
      "Location": "@prefix@/bin/sample-tool"
    },
    "sample-java": {
      "Type": "jar",
      "Location": "@prefix@/share/java/sample.jar"
    }
  }
}
