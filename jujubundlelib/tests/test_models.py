# Copyright 2015 Canonical Ltd.
# Licensed under the AGPLv3, see LICENCE file for details.

from __future__ import unicode_literals

import unittest

from jujubundlelib import models
from jujubundlelib.tests import helpers


class TestParseV3UnitPlacement(
        helpers.ValueErrorTestsMixin, unittest.TestCase):

    def test_success(self):
        self.assertEqual(
            models.UnitPlacement('', '', '', ''),
            models.parse_v3_unit_placement(''),
        )
        self.assertEqual(
            models.UnitPlacement('', '0', '', ''),
            models.parse_v3_unit_placement('0'),
        )
        self.assertEqual(
            models.UnitPlacement('', '', 'mysql', ''),
            models.parse_v3_unit_placement('mysql'),
        )
        self.assertEqual(
            models.UnitPlacement('lxc', '0', '', ''),
            models.parse_v3_unit_placement('lxc:0'),
        )
        self.assertEqual(
            models.UnitPlacement('', '', 'mysql', 1),
            models.parse_v3_unit_placement('mysql=1'),
        )
        self.assertEqual(
            models.UnitPlacement('lxc', '', 'mysql', 1),
            models.parse_v3_unit_placement('lxc:mysql=1'),
        )

    def test_failure(self):
        tests = (
            {
                'about': 'extra container',
                'placement': 'lxc:lxc:0',
                'error': b'placement lxc:lxc:0 is malformed, too many parts',
            },
            {
                'about': 'extra unit',
                'placement': 'mysql=0=0',
                'error': b'placement mysql=0=0 is malformed, too many parts',
            },
            {
                'about': 'bad container',
                'placement': 'asdf:0',
                'error': b'invalid container asdf for placement asdf:0',
            },
            {
                'about': 'bad unit',
                'placement': 'foo=a',
                'error': b'unit in placement foo=a must be digit',
            },
            {
                'about': 'place to machine other than bootstrap node',
                'placement': '1',
                'error': b'legacy bundles may not place units on machines '
                         b'other than 0',
            },
        )
        for test in tests:
            with self.assert_value_error(test['error'], test['about']):
                models.parse_v3_unit_placement(test['placement'])


class TestParseV4UnitPlacement(
        helpers.ValueErrorTestsMixin, unittest.TestCase):

    def test_success(self):
        self.assertEqual(
            models.UnitPlacement('', '', '', ''),
            models.parse_v4_unit_placement(''),
        )
        self.assertEqual(
            models.UnitPlacement('', '0', '', ''),
            models.parse_v4_unit_placement('0'),
        )
        self.assertEqual(
            models.UnitPlacement('', '', 'mysql', ''),
            models.parse_v4_unit_placement('mysql'),
        )
        self.assertEqual(
            models.UnitPlacement('lxc', '0', '', ''),
            models.parse_v4_unit_placement('lxc:0'),
        )
        self.assertEqual(
            models.UnitPlacement('', '', 'mysql', 1),
            models.parse_v4_unit_placement('mysql/1'),
        )
        self.assertEqual(
            models.UnitPlacement('lxc', '', 'mysql', 1),
            models.parse_v4_unit_placement('lxc:mysql/1'),
        )
        self.assertEqual(
            models.UnitPlacement('', 'new', '', ''),
            models.parse_v4_unit_placement('new'),
        )
        self.assertEqual(
            models.UnitPlacement('lxc', 'new', '', ''),
            models.parse_v4_unit_placement('lxc:new'),
        )

    def test_failure(self):
        tests = (
            {
                'about': 'extra container',
                'placement': 'lxc:lxc:0',
                'error': b'placement lxc:lxc:0 is malformed, too many parts',
            },
            {
                'about': 'extra unit',
                'placement': 'mysql/0/0',
                'error': b'placement mysql/0/0 is malformed, too many parts',
            },
            {
                'about': 'bad container',
                'placement': 'asdf:0',
                'error': b'invalid container asdf for placement asdf:0',
            },
            {
                'about': 'bad unit',
                'placement': 'foo/a',
                'error': b'unit in placement foo/a must be digit',
            },
        )
        for test in tests:
            with self.assert_value_error(test['error'], test['about']):
                models.parse_v4_unit_placement(test['placement'])


class TestNormalizeMachines(
        helpers.ValueErrorTestsMixin, unittest.TestCase):

    def test_success(self):
        provided = {
            '0': {
                'series': 'precise',
            },
            '1': {
                'series': 'trusty',
                'constraints': 'mem=foo',
            },
        }
        expected = {
            0: {
                'series': 'precise',
            },
            1: {
                'series': 'trusty',
                'constraints': 'mem=foo',
            },
        }
        self.assertEqual(models.normalize_machines(provided), expected)
        self.assertEqual(models.normalize_machines(expected), expected)

    def test_failure(self):
        with self.assert_value_error(b'Malformed machines None'):
            models.normalize_machines(None)
        with self.assert_value_error(b'Malformed machines bad-wolf'):
            models.normalize_machines('bad-wolf')
