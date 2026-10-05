import XCTest
@testable import KidsCharacterKit

final class KidsCharacterKitTests: XCTestCase {
    func testPackageBuildsAndImports() {
        XCTAssertEqual(KidsCharacterKitPackage.name, "KidsCharacterKit")
    }
}
