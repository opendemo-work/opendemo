package com.opendemo.java.maven;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class MavenStructureDemoTest {

    @Test
    void testMainRunsSuccessfully() {
        assertDoesNotThrow(() -> MavenStructureDemo.main(new String[]{}));
    }

    @Test
    void testProjectStructureInfo() {
        assertNotNull(MavenStructureDemo.class.getPackage());
        assertEquals("com.opendemo.java.maven", MavenStructureDemo.class.getPackageName());
    }
}
