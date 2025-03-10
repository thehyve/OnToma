from util import assert_result_ot_label
from ontoma import OnToma


def test_find_term_asthma(ontclient):
    assert_result_ot_label(
        ontclient.find_term('asthma'),
        ['MONDO_0004979']
    )


def test_is_included(ontclient):
    assert ontclient.filter_identifiers_by_efo_current(['MONDO:0018149']) == ['MONDO:0018149']


def test_suggest_hp_term_not_excluded(ontclient):
    assert_result_ot_label(
        ontclient.find_term('hypogammaglobulinemia'),
        ['MONDO_0015977']
    )


def test_catch_ordo(ontclient):
    assert_result_ot_label(
        ontclient.find_term('Camptodactyly-arthropathy-coxa-vara-pericarditis syndrome'),
        ['EFO_0009028']
    )
    assert_result_ot_label(
        ontclient.find_term('OMIM:208250', code=True),
        {'EFO_0009028'}
    )


def test_query_comma(ontclient):
    # The test deliberately expects no results, since a match from “3-methylglutaconic aciduria, type III” to
    # “Orphanet_67047” is obtained from fuzzy OLS lookup.
    assert not ontclient.find_term('3-methylglutaconic aciduria, type III')


def test_find_term_alzheimer(ontclient):

    assert_result_ot_label(
        ontclient.find_term('alzheimer\'s disease'),
        ['MONDO_0004975']
    )


def test_manually_mapped_in_recent_efo_releases():
    ontclient = OnToma(efo_release='v3.44.0', cache_dir='/tmp/efo_cache')
    assert_result_ot_label(
            ontclient.find_term('Z12 Special screening examination for neoplasms'),
            ['EFO_0021523']  # EFO ID for 'examination for neoplasm'
    )


def test_manual_mapping_too_new_for_efo_release():
    ontclient = OnToma(efo_release='v3.43.0', cache_dir='/tmp/efo_cache')
    assert_result_ot_label(
            ontclient.find_term('Z12 Special screening examination for neoplasms'),
            []  # EFO_0021523 did not exist in this release
    )


def test_manual_mapping_matching_old_efo():
    # TODO: find example that isn't too old to have an ot_release tag
    ontclient = OnToma(efo_release='v3.43.0', ot_release='22.08', cache_dir='/tmp/efo_cache')
    assert_result_ot_label(
            ontclient.find_term('Z12 Special screening examination for neoplasms'),
            ['EFO_0009517']  # EFO ID for 'checkup'
    )
