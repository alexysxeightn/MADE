from unittest.mock import patch
import pytest
from asset import print_asset_revenue, Asset


@pytest.fixture
def asset_filepath(tmpdir):
	asset_fileio = tmpdir.join("asset.txt")
	asset_fileio.write("property 1000000 0.1")
	asset_filepath_ = asset_fileio.strpath
	return asset_filepath_


@patch("asset.Asset")
def test_asset_calculate_revenue_always_return_100500(mock_asset_class, asset_filepath, capsys):
	mock_asset_class.calculate_revenue.return_value = 100500.0
	mock_asset_class.build_from_str.return_value = mock_asset_class

	periods = [1, 2, 5, 10]
	with open(asset_filepath) as asset_fin:
		print_asset_revenue(asset_fin, periods=periods)

	captured = capsys.readouterr()
	assert len(periods) == len(captured.out.splitlines())
	for line in captured.out.splitlines():
		assert "100500" in line


@patch("cbr.get_usd_course")
def test_can_mock_external_calls(mock_get_usd_course):
	mock_get_usd_course.side_effect = [76.54, 77.44, ConnectionError]

	asset_property = Asset(name="property", capital=10**6, interest=0.1)
	assert asset_property.calculate_revenue_from_usd(years=1) == pytest.approx(76.54 * 10**5, abs=0.01)
	assert asset_property.calculate_revenue_from_usd(years=1) == pytest.approx(77.44 * 10**5, abs=0.01)
	with pytest.raises(ConnectionError):
		asset_property.calculate_revenue_from_usd(years=1)


@patch("cbr.get_usd_course")
def test_can_mock_external_calls2(mock_get_usd_course):
	def generator():
		a = 76.32
		while True:
			yield a
			a += 0.1
	generator_usd_course = generator()
	mock_get_usd_course.side_effect = generator_usd_course

	asset_property = Asset(name="property", capital=10**6, interest=0.1)
	for iteration in range(6):
		expected_revenue = (76.32 + 0.1 * iteration) * asset_property.capital * asset_property.interest
		calculated_revenue = asset_property.calculate_revenue_from_usd(years=1)
		assert calculated_revenue == pytest.approx(expected_revenue, abs=0.01), (
			f"incorrect calculated revenue at iteration {iteration}"
		)