{
  "name": "sample",
  "description": "Sample CPS",
  "license": "BSD",
  "version": "1.2.0",
  "compat_version": "0.8.0",
  "platform": {
    "isa": "x86_64",
    "kernel": "linux",
    "c_runtime_vendor": "gnu",
    "c_runtime_version": "2.20",
    "jvm_version": "1.6"
  },
  "configurations": [ "optimized", "debug" ],
  "default_components": [ "sample" ],
  "components": {
    "sample-core": {
      "type": "interface",
      "definitions": [ "SAMPLE" ],
      "includes": [ "@prefix@/include" ]
    },
    "sample": {
      "type": "interface",
      "configurations": {
        "shared": {
          "requires": [ ":sample-shared" ]
        },
        "static": {
          "requires": [ ":sample-static" ]
        }
      }
    },
    "sample-shared": {
      "type": "dylib",
      "requires": [ ":sample-core" ],
      "configurations": {
        "optimized": {
          "location": "@prefix@/lib64/libsample.so.1.2.0"
        },
        "debug": {
          "location": "@prefix@/lib64/libsample_d.so.1.2.0"
        }
      }
    },
    "sample-static": {
      "type": "archive",
      "definitions": [ "SAMPLE_STATIC" ],
      "requires": [ ":sample-core" ],
      "configurations": {
        "optimized": {
          "location": "@prefix@/lib64/libsample.a"
        },
        "debug": {
          "location": "@prefix@/lib64/libsample_d.a"
        }
      }
    },
    "sample-tool": {
      "type": "executable",
      "location": "@prefix@/bin/sample-tool"
    },
    "sample-java": {
      "type": "jar",
      "location": "@prefix@/share/java/sample.jar"
    }
  }
}
