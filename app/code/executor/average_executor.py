from nvflare.apis.executor import Executor
from nvflare.apis.fl_constant import FLContextKey
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable
from nvflare.apis.signal import Signal

from .local_average import get_local_average_and_count
import json
import os


class AverageExecutor(Executor):
    def execute(
        self,
        task_name: str,
        shareable: Shareable,
        fl_ctx: FLContext,
        abort_signal: Signal,
    ) -> Shareable:

        if task_name == "get_local_average_and_count":
            data_dir_path = get_data_dir_path(fl_ctx)
            computation_parameters = fl_ctx.get_peer_context().get_prop("COMPUTATION_PARAMETERS")
            decimal_places = computation_parameters["decimal_places"]
            local_average_and_count = get_local_average_and_count(
                data_dir_path, decimal_places)

            # save local average to local results file
            save_results_to_file(
                local_average_and_count,
                "local_average.json",
                fl_ctx
            )

            outgoing_shareable = Shareable()
            outgoing_shareable["result"] = local_average_and_count
            return outgoing_shareable

        if task_name == "accept_global_average":
            # save global average to local results file
            result = {"global_average": shareable.get("global_average", {})}
            save_results_to_file(
                result,
                "global_average.json",
                fl_ctx
            )
            return Shareable()


def save_results_to_file(results: dict, file_name: str, fl_ctx: FLContext):
    results_dir = get_results_dir_path(fl_ctx)
    print(f"\nSaving results to: {results_dir}\n")
    with open(os.path.join(results_dir, file_name), "w") as f:
        json.dump(results, f)


def get_results_dir_path(fl_ctx: FLContext) -> str:
    """
    Determines the appropriate results directory path for the federated learning application by checking
    if in production, simulator, or POC (Proof of Concept) mode.
    """

    # Define paths for production (from environment), simulator, and POC modes.
    job_id = fl_ctx.get_job_id()
    site_name = fl_ctx.get_prop(FLContextKey.CLIENT_NAME)

    production_path = os.getenv("RESULTS_DIR")
    simulator_base_path = os.path.abspath(
        os.path.join(os.getcwd(), "../../../test_results"))
    poc_base_path = os.path.abspath(os.path.join(
        os.getcwd(), "../../../../test_results"))
    simulator_path = os.path.join(simulator_base_path, job_id, site_name)
    poc_path = os.path.join(poc_base_path, job_id, site_name)

    # Check for the environment path first, then simulator, and lastly POC path.
    if production_path:
        return production_path
    if os.path.exists(simulator_base_path):
        os.makedirs(simulator_path, exist_ok=True)
        return simulator_path
    if os.path.exists(poc_base_path):
        os.makedirs(poc_path, exist_ok=True)
        return poc_path

    # Raise an error if no path is found.
    raise FileNotFoundError("Results directory path could not be determined.")


def get_data_dir_path(fl_ctx: FLContext) -> str:
    """
    Determines the appropriate data directory path for the federated learning application by checking
    if in production, simulator, or poc mode.
    """

    # Define paths for production (from environment), simulator, and POC modes.
    site_name = fl_ctx.get_prop(FLContextKey.CLIENT_NAME)


    production_path = os.getenv("DATA_DIR")
    simulator_path = os.path.abspath(os.path.join(os.getcwd(), "../../../test_data", site_name))
    poc_path = os.path.abspath(os.path.join(os.getcwd(), "../../../../test_data", site_name))

    # Check for the environment path first, then simulator, and lastly POC path.
    if production_path:
        return production_path
    if os.path.exists(simulator_path):
        return simulator_path
    if os.path.exists(poc_path):
        return poc_path

    # Raise an error if no path is found.
    raise FileNotFoundError("Data directory path could not be determined.")
