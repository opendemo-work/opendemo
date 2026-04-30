package com.opendemo.java.refactoring;

import com.opendemo.java.refactoring.before.*;
import com.opendemo.java.refactoring.after.*;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.time.LocalDate;
import java.util.Arrays;

class RefactoringPatternsTest {
    @Test
    void extractMethodSameBehavior() {
        ExtractMethodBefore.Order o1 = new ExtractMethodBefore.Order(100.0);
        ExtractMethodBefore.Order o2 = new ExtractMethodBefore.Order(200.0);

        ExtractMethodBefore before = new ExtractMethodBefore("Alice", Arrays.asList(o1, o2));
        ExtractMethodAfter after = new ExtractMethodAfter("Alice", Arrays.asList(o1, o2));

        java.io.ByteArrayOutputStream baos1 = new java.io.ByteArrayOutputStream();
        System.setOut(new java.io.PrintStream(baos1));
        before.printOwing();
        String beforeOutput = baos1.toString();

        java.io.ByteArrayOutputStream baos2 = new java.io.ByteArrayOutputStream();
        System.setOut(new java.io.PrintStream(baos2));
        after.printOwing();
        String afterOutput = baos2.toString();

        assertEquals(beforeOutput, afterOutput);
        System.setOut(System.out);
    }

    @Test
    void replaceConditionalSameResults() {
        ReplaceConditionalBefore before = new ReplaceConditionalBefore();
        ReplaceConditionalAfter after = new ReplaceConditionalAfter();

        assertEquals(before.calculatePrice("NORMAL", 100.0), after.calculatePrice("NORMAL", 100.0), 0.001);
        assertEquals(before.calculatePrice("VIP", 100.0), after.calculatePrice("VIP", 100.0), 0.001);
        assertEquals(before.calculatePrice("STAFF", 100.0), after.calculatePrice("STAFF", 100.0), 0.001);
        assertEquals(before.calculatePrice("PREMIUM", 100.0), after.calculatePrice("PREMIUM", 100.0), 0.001);
        assertEquals(before.getLabel("VIP"), after.getLabel("VIP"));
    }

    @Test
    void introduceParameterObjectSameBehavior() {
        IntroduceParameterObjectBefore before = new IntroduceParameterObjectBefore();
        CustomerInfo info = new CustomerInfo("Alice", "Smith", 30, "123 Main", "NYC", "10001", "555-1234", "a@b.com");
        IntroduceParameterObjectAfter after = new IntroduceParameterObjectAfter();

        assertTrue(before.isValidCustomer("Alice", "Smith", 30, "123 Main", "NYC", "10001", "555-1234", "a@b.com"));
        assertTrue(after.isValidCustomer(info));

        assertEquals("Hello, Alice Smith!", before.getGreeting("Alice", "Smith", 30, "123 Main", "NYC", "10001", "555-1234", "a@b.com"));
        assertEquals("Hello, Alice Smith!", after.getGreeting(info));
    }

    @Test
    void replaceMagicNumberSameResults() {
        ReplaceMagicNumberBefore before = new ReplaceMagicNumberBefore();
        ReplaceMagicNumberAfter after = new ReplaceMagicNumberAfter();

        assertEquals(before.calculateShipping(0.5, "DOMESTIC"), after.calculateShipping(0.5, "DOMESTIC"), 0.001);
        assertEquals(before.calculateShipping(3.0, "DOMESTIC"), after.calculateShipping(3.0, "DOMESTIC"), 0.001);
        assertEquals(before.calculateShipping(3.0, "INTERNATIONAL"), after.calculateShipping(3.0, "INTERNATIONAL"), 0.001);
        assertEquals(before.calculateShipping(15.0, "DOMESTIC"), after.calculateShipping(15.0, "DOMESTIC"), 0.001);
        assertTrue(before.isFreeShippingEligible(35.0));
        assertTrue(after.isFreeShippingEligible(35.0));
        assertFalse(after.isFreeShippingEligible(34.99));
    }

    @Test
    void decomposeConditionalSameResults() {
        LocalDate summerDate = LocalDate.of(2025, 7, 15);
        LocalDate winterDate = LocalDate.of(2025, 12, 15);
        LocalDate offDate = LocalDate.of(2025, 4, 15);
        double rate = 10.0;

        DecomposeConditionalBefore beforeSummer = new DecomposeConditionalBefore(summerDate, rate);
        DecomposeConditionalAfter afterSummer = new DecomposeConditionalAfter(summerDate, rate);
        assertEquals(beforeSummer.calculateCharge(5.0), afterSummer.calculateCharge(5.0), 0.001);
        assertEquals("Summer", afterSummer.getSeason());

        DecomposeConditionalBefore beforeWinter = new DecomposeConditionalBefore(winterDate, rate);
        DecomposeConditionalAfter afterWinter = new DecomposeConditionalAfter(winterDate, rate);
        assertEquals(beforeWinter.calculateCharge(5.0), afterWinter.calculateCharge(5.0), 0.001);
        assertEquals("Winter", afterWinter.getSeason());

        DecomposeConditionalBefore beforeOff = new DecomposeConditionalBefore(offDate, rate);
        DecomposeConditionalAfter afterOff = new DecomposeConditionalAfter(offDate, rate);
        assertEquals(beforeOff.calculateCharge(5.0), afterOff.calculateCharge(5.0), 0.001);
        assertEquals("Off-season", afterOff.getSeason());
    }

    @Test
    void customerInfoHelpers() {
        CustomerInfo info = new CustomerInfo("Bob", "Jones", 25, "456 Oak", "LA", "90001", "555-9999", "b@c.com");
        assertEquals("Bob Jones", info.getFullName());
        assertEquals("456 Oak, LA 90001", info.getAddress());
    }

    @Test
    void pricingStrategyInterface() {
        PricingStrategy normal = new NormalPricing();
        PricingStrategy vip = new VipPricing();
        PricingStrategy staff = new StaffPricing();
        PricingStrategy premium = new PremiumPricing();

        assertEquals(100.0, normal.calculatePrice(100.0), 0.001);
        assertEquals(80.0, vip.calculatePrice(100.0), 0.001);
        assertEquals(50.0, staff.calculatePrice(100.0), 0.001);
        assertEquals(70.0, premium.calculatePrice(100.0), 0.001);
    }
}
