import logging
from .parameter import HierarchicalParameter

logger = logging.getLogger(__name__)


class HierarchicalProblem:

    def __init__(self, xs = None):
        """
        s_ids, b_ids, sigma_ids should all be estimated parameters.
        """
        if xs is None:
            xs = []
        self.xs = xs

    @staticmethod
    def from_parameter_df(df):
        """
        Create list of hierarchical parameters from parameter df
        based on name conventions.
        """
        # create list of hierarchical parameters
        xs = []
        for ix, x in enumerate(df.reset_index()['parameterId']):
            type_ = None
            default_val_ = None
            if df.reset_index()['hierarchicalOptimization'][ix]:
                if df.reset_index()['parameterType'][ix] == 'scaling':
                    type_ = HierarchicalParameter.SCALING
                    default_val_ = 1.0
                elif df.reset_index()['parameterType'][ix] == 'offset':
                    type_ = HierarchicalParameter.OFFSET
                    default_val_ = 0.0
                elif df.reset_index()['parameterType'][ix] == 'sigma':
                    type_ = HierarchicalParameter.SIGMA
                    default_val_ = 1.0
            if type_:
                x = HierarchicalParameter(
                    id_=x, ix_=ix, type_=type_, default_val_=default_val_)
                xs.append(x)

        # create problem
        return HierarchicalProblem(xs)


    def get_x_ids(self):
        return [x.id for x in self.xs]

    def get_x_by_id(self, id_):
        for x in self.xs:
            if x.id == id_:
                return x
        return None
    
    def get_xs_for_type(self, type_):
        return [x for x in self.xs if x.type == type_]

    def insert_for_id(self, id_, condition_ix, time_ix, observable_ix):
        x = self.get_x_by_id(id_)
        if x:
            x.append(condition_ix, time_ix, observable_ix)

    def is_empty(self):
        return len(self.xs) == 0

    def get_all_ixs_and_default_vals(self):
        ixs = self.s_ixs + self.b_ixs + self.sigma_ixs
        default_vals = [1.0] * len(self.s_ids) + [0.0] * len(self.b_ids) + [1.0] * len(self.sigma_ids)
        return ixs, default_vals

    def validate(self):
        """
        Check that assumptions are fulfilled.
        """
        self._validate_scaling_and_offset()

    def _validate_scaling_and_offset(self):
        """
        Requirement: For every scaling, all associated data points must either
        have no offset, or all the same offset.
        The same is required the other way round, i.e. scalings and offsets
        must be associated with the same data points.
        """
        pass

    def _validate_scaling_and_sigma(self):
        """
        Requirement: For every scaling, all associated data points must
        bla bla.
        """
        pass
