// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "KidsCharacterKit",
    platforms: [
        .iOS(.v16),
        .macOS(.v13),
    ],
    products: [
        .library(name: "KidsCharacterKit", targets: ["KidsCharacterKit"]),
    ],
    targets: [
        .target(name: "KidsCharacterKit"),
        .testTarget(
            name: "KidsCharacterKitTests",
            dependencies: ["KidsCharacterKit"]
        ),
    ]
)
