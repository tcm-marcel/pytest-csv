# ----------------------------------------------------------------------
# pytest-csv - https://github.com/nicoulaj/pytest-csv
# copyright (c) 2018 pytest-csv contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------

from pytest_csv.column import *
from ._utils import assert_csv_equal, assert_outcomes


def test_passed(testdir):
    testdir.makepyfile('''
        def test_01():
            assert True
    ''')

    result = testdir.runpytest('--csv', 'tests.csv', '--csv-columns', 'success')

    assert_outcomes(result, passed=1)

    assert_csv_equal('tests.csv', [
        (SUCCESS, 'True'),
    ])


def test_failed(testdir):
    testdir.makepyfile('''
        def test_01():
            assert False
    ''')

    result = testdir.runpytest('--csv', 'tests.csv', '--csv-columns', 'success')

    assert_outcomes(result, failed=1)

    assert_csv_equal('tests.csv', [
        (SUCCESS, 'False'),
    ])


def test_error(testdir):
    testdir.makepyfile('''
        import pytest
    
        @pytest.fixture
        def some_fixture():
            raise Exception('this fixture is broken')
    
        def test_01(some_fixture):
            pass
    ''')

    result = testdir.runpytest('--csv', 'tests.csv', '--csv-columns', 'success')

    assert_outcomes(result, error=1)

    assert_csv_equal('tests.csv', [
        (SUCCESS, 'False'),
    ])


def test_skipped(testdir):
    testdir.makepyfile('''
        import pytest

        @pytest.mark.skip
        def test_01():
            pass
    ''')

    result = testdir.runpytest('--csv', 'tests.csv', '--csv-columns', 'success')

    assert_outcomes(result, skipped=1)

    assert_csv_equal('tests.csv', [
        (SUCCESS, 'True'),
    ])


def test_xfail(testdir):
    testdir.makepyfile('''
        import pytest

        @pytest.mark.xfail
        def test_01():
            raise Exception()
    ''')

    result = testdir.runpytest('--csv', 'tests.csv', '--csv-columns', 'success')

    assert_outcomes(result, xfailed=1)

    assert_csv_equal('tests.csv', [
        (SUCCESS, 'True'),
    ])


def test_xpassed(testdir):
    testdir.makepyfile('''
        import pytest

        @pytest.mark.xfail
        def test_01():
            pass
    ''')

    result = testdir.runpytest('--csv', 'tests.csv', '--csv-columns', 'success')

    assert_outcomes(result, xpassed=1)

    assert_csv_equal('tests.csv', [
        (SUCCESS, 'True'),
    ])
