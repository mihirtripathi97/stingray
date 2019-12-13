import pytest
import numpy as np
from stingray.deadtime.filters import filter_for_deadtime
from stingray.events import EventList


def test_filter_for_deadtime_nonpar():
    """Test dead time filter, non-paralyzable case."""
    events = np.array([1, 1.05, 1.07, 1.08, 1.1, 2, 2.2, 3, 3.1, 3.2])
    filt_events = filter_for_deadtime(events, 0.11)
    expected = np.array([1, 2, 2.2, 3, 3.2])
    assert np.all(filt_events == expected), \
        "Wrong: {} vs {}".format(filt_events, expected)


def test_filter_for_deadtime_evlist():
    """Test dead time filter, non-paralyzable case."""
    events = np.array([1, 1.05, 1.07, 1.08, 1.1, 2, 2.2, 3, 3.1, 3.2])
    events = EventList(events, pi=np.random.randint(events.size))
    events.mjdref = 10
    with pytest.warns(UserWarning) as record:
        filt_events = filter_for_deadtime(events, 0.11)
    assert np.any(["PI information is lost during dead time filterin"
                   in r.message.args[0] for r in record])
    expected = np.array([1, 2, 2.2, 3, 3.2])
    assert np.all(filt_events.time == expected), \
        "Wrong: {} vs {}".format(filt_events, expected)


def test_filter_for_deadtime_lt0():
    """Test dead time filter, non-paralyzable case."""
    events = np.array([1, 1.05, 1.07, 1.08, 1.1, 2, 2.2, 3, 3.1, 3.2])
    with pytest.warns(UserWarning) as record:
        evlist = filter_for_deadtime(events, -0.11)

    assert np.any(["Dead time < 0"
                   in r.message.args[0] for r in record])


def test_filter_for_deadtime_nonpar_sigma():
    """Test dead time filter, non-paralyzable case."""
    events = np.array([1, 1.05, 1.07, 1.08, 1.1, 2, 2.2, 3, 3.1, 3.2])
    filt_events = filter_for_deadtime(events, 0.11, dt_sigma=0.001)
    expected = np.array([1, 2, 2.2, 3, 3.2])
    assert np.all(filt_events == expected), \
        "Wrong: {} vs {}".format(filt_events, expected)


def test_filter_for_deadtime_nonpar_bkg():
    """Test dead time filter, non-paralyzable case, with background."""
    events = np.array([1.1, 2, 2.2, 3, 3.2])
    bkg_events = np.array([1, 3.1])
    filt_events, info = \
        filter_for_deadtime(events, 0.11, bkg_ev_list=bkg_events,
                            return_all=True)
    expected_ev = np.array([2, 2.2, 3, 3.2])
    expected_bk = np.array([1])
    assert np.all(filt_events == expected_ev), \
        "Wrong: {} vs {}".format(filt_events, expected_ev)
    assert np.all(info.bkg == expected_bk), \
        "Wrong: {} vs {}".format(info.bkg, expected_bk)


def test_filter_for_deadtime_par():
    """Test dead time filter, paralyzable case."""
    events = np.array([1, 1.1, 2, 2.2, 3, 3.1, 3.2])
    assert np.all(filter_for_deadtime(
        events, 0.11, paralyzable=True) == np.array([1, 2, 2.2, 3]))


def test_filter_for_deadtime_par_bkg():
    """Test dead time filter, paralyzable case, with background."""
    events = np.array([1.1, 2, 2.2, 3, 3.2])
    bkg_events = np.array([1, 3.1])
    filt_events, info = \
        filter_for_deadtime(events, 0.11, bkg_ev_list=bkg_events,
                            paralyzable=True, return_all=True)
    expected_ev = np.array([2, 2.2, 3])
    expected_bk = np.array([1])
    assert np.all(filt_events == expected_ev), \
        "Wrong: {} vs {}".format(filt_events, expected_ev)
    assert np.all(info.bkg == expected_bk), \
        "Wrong: {} vs {}".format(info.bkg, expected_bk)


def test_deadtime_mask_par():
    """Test dead time filter, paralyzable case, with background."""
    events = np.array([1.1, 2, 2.2, 3, 3.2])
    bkg_events = np.array([1, 3.1])
    filt_events, info = \
        filter_for_deadtime(events, 0.11, bkg_ev_list=bkg_events,
                            paralyzable=True, return_all=True)

    assert np.all(filt_events == events[info.mask])
