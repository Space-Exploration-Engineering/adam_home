import pytest

from adam import PropagationParams, OpmParams
from adam.adam_processing_service import ApsResults, BatchPropagationResults


class TestAdamProcessingService:

    def test_submit_batch(self, service):
        keplerian_elements = {
            'semi_major_axis_km': 448793612,
            'eccentricity': 0.1,
            'inclination_deg': 90,
            'ra_of_asc_node_deg': 91,
            'arg_of_pericenter_deg': 92,
            'true_anomaly_deg': 93,
            'gm': 132712440041.9394
        }

        keplerian_sigma = {
            'semi_major_axis': 100,
            'eccentricity': 0.001,
            'inclination': 1,
            'ra_of_asc_node': 2,
            'arg_of_pericenter': 3,
            'true_anomaly': 4,
        }

        # state_vec = [130347560.13690618,
        #              -74407287.6018632,
        #              -35247598.541470632,
        #              23.935241263310683,
        #              27.146279819258538,
        #              10.346605942591514]
        # sigma_vec = {'x': 1000,
        #              'y': 1001,
        #              'z': 1002,
        #              'x_dot': 10,
        #              'y_dot': 11,
        #              'z_dot': 12}
        draws = 5
        propagation_params = PropagationParams({
            'start_time': '2017-10-04T00:00:00Z',  # propagation start time in ISO format
            'end_time': '2017-10-11T00:00:00Z',  # propagation end time in ISO format

            'project_uuid': service.workspace,
            'keplerianSigma': keplerian_sigma,
            'monteCarloDraws': draws,
            'propagationType': 'MONTE_CARLO',
            'description': 'Unit Test Run',
            'stopOnImpact': True,
            'step_size': 86400,
            'stopOnCloseApproach': False,
            'stopOnImpactDistanceMeters': 500000,
            'closeApproachRadiusFromTargetMeters': 7000000000
        })

        opm_params = OpmParams({
            'epoch': '2017-10-04T00:00:00Z',
            'keplerian_elements': keplerian_elements,
        })

        response = service.processing_service.execute_batch_propagation(
            service.workspace, propagation_params, opm_params)
        assert response.job_id() is not None


@pytest.mark.skip(reason="make tests assert and create actual job ids")
class TestApsResultClass:

    def test_get_status(self, service):
        results = ApsResults.fromRESTwithRawIds(
            service.rest, service.workspace, '31a02f1b-0398-431f-b048-c9c9aa5128e4')
        print(results.check_status())

    def test_get_empty_results(self, service):
        with pytest.raises(RuntimeError):
            results = ApsResults.fromRESTwithRawIds(
                service.rest, service.workspace, '31a02f1b-0398-431f-b048-c9c9aa5128e4')
            print(results.get_results())

    # def test_wait_for_complete(self):
    # results = ApsResults.fromRESTwithRawIds(
    #    self.rest, self.workspace, '18937261-1973-4a77-8e2c-c02e8afe0d45')
    # results.wait_for_complete(60, True)


@pytest.mark.skip(reason="make tests assert and create actual job ids")
class TestBatchPropagationResultClass:

    def test_get_summary(self, service):
        results = BatchPropagationResults.fromRESTwithRawIds(
            service.rest,
            '0dc1e8b0-4f92-46ad-8838-c9e9eca6935c',
            '285332fd-91e9-4e48-843d-36495caaf915')
        summary = results.get_summary()
        print(summary)

    def test_get_final_positions(self, service):
        results = BatchPropagationResults.fromRESTwithRawIds(
            service.rest,
            '0dc1e8b0-4f92-46ad-8838-c9e9eca6935c',
            '285332fd-91e9-4e48-843d-36495caaf915')
        print("Misses: ")
        print(results.get_final_positions(BatchPropagationResults.PositionOrbitType.MISS))

        print("Close Approaches: ")
        print(results.get_final_positions(BatchPropagationResults.PositionOrbitType.CLOSE_APPROACH))

        print("Impacts:")
        print(results.get_final_positions(BatchPropagationResults.PositionOrbitType.IMPACT))

    def test_get_result_ephemeris_count(self, service):
        results = BatchPropagationResults.fromRESTwithRawIds(
            service.rest,
            '0dc1e8b0-4f92-46ad-8838-c9e9eca6935c',
            '285332fd-91e9-4e48-843d-36495caaf915')
        print(results.get_result_ephemeris_count())

    def test_get_result_ephemeris(self, service):
        results = BatchPropagationResults.fromRESTwithRawIds(
            service.rest,
            '0dc1e8b0-4f92-46ad-8838-c9e9eca6935c',
            '285332fd-91e9-4e48-843d-36495caaf915')
        print(results.get_result_ephemeris(2))
