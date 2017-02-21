{
  "Name": "sample",
  "Description": "Sample CPS",
  "License": "BSD",
  "Version": "1.2.0",
  "Compat-Version": "0.8.0",
  "Configurations": [ "Optimized", "Debug" ],
  "Default-Components": [ "sample" ],
  "Components": {
    "sample-core": {
      "Type": "interface",
      "Definitions": [ "SAMPLE" ],
      "Includes": [ "@prefix@/include" ]
    },
    "sample": {
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
