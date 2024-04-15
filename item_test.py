import unittest
from item import *


class MyTestCase(unittest.TestCase):

    def test_generic(self):
        item = Item()

        self.assertEqual(item.name, "Unknown Item")
        self.assertEqual(item.description, "Indescribable")
        self.assertEqual(item.type, ItemTypes.ITEM)
        self.assertEqual(item.attributeValue, 0)

    def test_genericAndName(self):
        item = Item(name="Mjolnir")

        self.assertEqual(item.name, "Mjolnir")
        self.assertEqual(item.description, "Indescribable")
        self.assertEqual(item.type, ItemTypes.ITEM)
        self.assertEqual(item.attributeValue, 0)

    def test_genericAndDesc(self):
        item = Item(description="Godly")

        self.assertEqual(item.name, "Unknown Item")
        self.assertEqual(item.description, "Godly")
        self.assertEqual(item.type, ItemTypes.ITEM)
        self.assertEqual(item.attributeValue, 0)

    def test_genericAndAttribute(self):
        item = Item(attribute_value=99)

        self.assertEqual(item.name, "Unknown Item")
        self.assertEqual(item.description, "Indescribable")
        self.assertEqual(item.type, ItemTypes.ITEM)
        self.assertEqual(item.attributeValue, 99)

    def test_generateItem_MELEE(self):
        # Run the test many times to ensure functionality
        for i in range(50):
            item = Item()
            item.generateItem(ItemTypes.MELEE)

            self.assertNotEqual(item.name, "Unknown Item")
            self.assertNotEqual(item.description, "Indescribable")
            self.assertEqual(item.type, ItemTypes.MELEE)
            self.assertNotEqual(item.attributeValue, 0)

    def test_generateItem_RANGED(self):
        # Run the test many times to ensure functionality
        for i in range(50):
            item = Item()
            item.generateItem(ItemTypes.RANGED)

            self.assertNotEqual(item.name, "Unknown Item")
            self.assertNotEqual(item.description, "Indescribable")
            self.assertEqual(item.type, ItemTypes.RANGED)
            self.assertNotEqual(item.attributeValue, 0)

    def test_generateItem_SHIELD(self):
        # Run the test many times to ensure functionality
        for i in range(50):
            item = Item()
            item.generateItem(ItemTypes.SHIELD)

            self.assertNotEqual(item.name, "Unknown Item")
            self.assertNotEqual(item.description, "Indescribable")
            self.assertEqual(item.type, ItemTypes.SHIELD)
            self.assertNotEqual(item.attributeValue, 0)

    def test_generateItem_POTION(self):
        # Run the test many times to ensure functionality
        for i in range(50):
            item = Item()
            item.generateItem(ItemTypes.POTION)

            self.assertNotEqual(item.name, "Unknown Item")
            self.assertNotEqual(item.description, "Indescribable")
            self.assertEqual(item.type, ItemTypes.POTION)
            self.assertNotEqual(item.attributeValue, 0)

    def test_generateItem_ITEM(self):
        # Run the test many times to ensure functionality
        for i in range(50):
            item = Item()
            item.generateItem(ItemTypes.ITEM)

            self.assertNotEqual(item.name, "Unknown Item")
            self.assertNotEqual(item.description, "Indescribable")
            self.assertEqual(item.type, ItemTypes.ITEM)
            self.assertEqual(item.attributeValue, 0)

    def test_generateItem_ARMOUR(self):
        # Run the test many times to ensure functionality
        for i in range(50):
            item = Item()
            item.generateItem(ItemTypes.ARMOUR)

            self.assertNotEqual(item.name, "Unknown Item")
            self.assertNotEqual(item.description, "Indescribable")
            self.assertEqual(item.type, ItemTypes.ARMOUR)
            self.assertNotEqual(item.attributeValue, 0)

    def test_generateItem_KEY(self):
        # Run the test many times to ensure functionality
        for i in range(50):
            item = Item()
            item.generateItem(ItemTypes.KEY)

            self.assertNotEqual(item.name, "Unknown Item")
            self.assertNotEqual(item.description, "Indescribable")
            self.assertEqual(item.type, ItemTypes.KEY)
            self.assertEqual(item.attributeValue, 0)

    def test_displayMELEE(self):
        item = Item()
        item.generateItem(ItemTypes.MELEE)

        expectedString = f"--~= {item.name} =~--\n{item.description}\n\nAttack: {item.attributeValue}"
        self.assertEqual(item.display(), expectedString)

    def test_displaySHIELD(self):
        item = Item()
        item.generateItem(ItemTypes.SHIELD)

        expectedString = f"--~= {item.name} =~--\n{item.description}\n\nDefense: {item.attributeValue}"
        self.assertEqual(item.display(), expectedString)

    def test_displayITEM(self):
        item = Item()
        item.generateItem(ItemTypes.ITEM)

        expectedString = f"--~= {item.name} =~--\n{item.description}\n"
        self.assertEqual(item.display(), expectedString)

    def test_get_attribute_static(self):
        item = Item()
        item.generateItem()
        item.attributeValue = 10

        self.assertEqual(item.get_attribute(), 10)

    def test_get_attribute_range(self):
        item = Item()
        item.generateItem()
        item.attributeValue = [10, 20]

        self.assertGreaterEqual(item.get_attribute(), 10)
        self.assertLessEqual(item.get_attribute(), 20)


    def test_str_cast(self):
        item = Item()
        item.generateItem(ItemTypes.ITEM)

        expectedString = f"{item.name}: {item.description} ({item.type.name})"
        self.assertEqual(str(item), expectedString)


if __name__ == '__main__':
    unittest.main()
