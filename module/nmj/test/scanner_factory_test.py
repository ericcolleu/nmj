# -*- coding: utf-8 -*-
from nmj.scanner_factory import ScannerFactory, ScannerNotFound
import mox
import unittest

class ScannerFactoryTestCase(mox.MoxTestBase):
	def test_01a(self):
		"""ScanFactory: register scanner"""
		scanner = "dummy scanner"
		factory = ScannerFactory()
		factory.register_scanner(scanner)
		self.assertEqual(factory.scanners, [scanner, ])

	def test_02a(self):
		"""ScanFactory: get_scanner, scanner found"""
		scanner1 = self.mox.CreateMockAnything()
		scanner2 = self.mox.CreateMockAnything()
		filepath = "/path/to/the/file"
		scanner1.accept(filepath).AndReturn(False)
		scanner2.accept(filepath).AndReturn(True)
		self.mox.ReplayAll()
		factory = ScannerFactory()
		factory.register_scanner(scanner1, scanner2)
		self.assertEqual(scanner2, factory.get_scanner(filepath))

	def test_03a(self):
		"ScannerFactory: get scanner, scanner not found"
		scanner1 = self.mox.CreateMockAnything()
		scanner2 = self.mox.CreateMockAnything()
		filepath = "/path/to/the/file"
		scanner1.accept(filepath).AndReturn(False)
		scanner2.accept(filepath).AndReturn(False)
		self.mox.ReplayAll()
		factory = ScannerFactory()
		factory.register_scanner(scanner1, scanner2)
		self.assertRaises(ScannerNotFound, factory.get_scanner, filepath)

if __name__ == "__main__":
	unittest.main()


