import argparse
from subsetter.utils.path import make_full_path
from subsetter.utils.parameters  import Parameters as Param
import os


def make_full_paths(args):
    args.ind = make_full_path(args.data_folder, args.ind)
    args.sample = make_full_path(args.data_folder, args.sample)
    args.loc = make_full_path(args.data_folder, args.loc)

    if args.sd is not None:
        args.sd = make_full_path(args.data_folder, args.sd)

    if not os.path.exists(args.analysis_folder):
        os.makedirs(args.analysis_folder)

    if args.output_folder is None:
        args.output_folder = make_full_path(args.analysis_folder,
                                            'output')
    else:
        args.output_folder = make_full_path(args.analysis_folder,
                                            args.output_folder)
    if not os.path.exists(args.output_folder):
        os.makedirs(args.output_folder)
    for nd in args.nDemes:
        if not os.path.exists("%s/%s" % (args.output_folder, nd)):
            os.makedirs("%s/%s" % (args.output_folder, nd))
        for nr in range(int(args.n_runs)):
            if not os.path.exists("%s/%s_run%s" % (args.output_folder, nd, nr)):
                os.makedirs("%s/%s_run%s" % (args.output_folder, nd, nr))

    if args.input_folder is None:
        args.input_folder = make_full_path(args.analysis_folder,
                                           'input')
    else:
        args.input_folder = make_full_path(args.analysis_folder,
                                            args.input_folder)
    if not os.path.exists(args.input_folder):
        os.makedirs(args.input_folder)

    if args.tmp_folder is None:
        args.tmp_folder = make_full_path(args.analysis_folder,
                                         'tmp')
    if not os.path.exists(args.tmp_folder):
        os.makedirs(args.tmp_folder)

    args.proj = make_full_path(args.input_folder, args.proj)

#    global TMP_PLINK
#    TMP_PLINK = make_full_path(args.tmp_folder, 'tmp_plink')


class Parameters(Param):
    """ class that handles parameters I/O

    the main idea is that this class unifies the different ways a project can
    be loaded. Current options are:
        - a dict like object, passed to init
        - from an input file
        - from the command line
        
    the main input format is from the command line
    """

    def __init__(self, **kwargs):
        Parameters.create_parser()
        for k, v in kwargs.items():
            setattr(self, k, v)

    @staticmethod
    def create_parser_eems(parser):
        parser.add_argument('--grid', default=0, help="""
                            If a custom grid (with earth curvature)
                            should be used. If yes, the population grid
                            is calculated from a precalcualted set of 3 
                            grids with different densities. Set parameter 
                            to 100, 250 or 500 for highest to lowest number 
                            of grid. 0 uses builtin grid.
                            """)
        parser.add_argument('--nDemes',
                            default=[100], nargs='*',
                            help="""eems arg: number of demes in the model
                            (default: 100 )"""
                            )
        parser.add_argument('--diploid',
                            default='true',
                            help="""eems arg: is diploid? (true/false)
                            (default: true )"""
                            )
        parser.add_argument('--numMCMCIter', '--n_mcmc', '--n-mcmc',
                            default=20000,
                            help="""eems arg: number of MCMC iterations
                            (default: 20000 )"""
                            )
        parser.add_argument('--numBurnIter', '--n_burn', '--n-burn',
                            default=10000,
                            help="""eems arg: number of burn in steps
                            (default: 10000 )"""
                            )
        parser.add_argument('--numThinIter', '--n_thin', '--n-thin',
                            default=99,
                            help="""eems arg: thinning interval
                            (default: 99 )"""
                            )
        parser.add_argument('--negBiSize',
                            default=10,
                            help="""eems arg
                            (default: 10 )"""
                            )
        parser.add_argument('--negBiProb',
                            default=0.67,
                            help="""eems arg
                            (default: 0.67 )"""
                            )
        parser.add_argument('--mrateShape',
                            default=0.001,
                            help="""eems arg
                            (default: 0.001 )"""
                            )
        parser.add_argument('--qrateShape',
                            default=0.001,
                            help="""eems arg
                            (default: 0.001 )"""
                            )
        parser.add_argument('--s2locShape',
                            default=0.001,
                            help="""eems arg
                            (default: 0.001 )"""
                            )
        parser.add_argument('--qrateScale',
                            default=1,
                            help="""eems arg
                            (default: 1 )"""
                            )
        parser.add_argument('--mrateScale',
                            default=1,
                            help="""eems arg
                            (default: 1 )"""
                            )
        parser.add_argument('--s2rateScale',
                            default=1,
                            help="""eems arg
                            (default: 1 )"""
                            )
        parser.add_argument('--mSeedsProposalS2',
                            default=0.01,
                            help="""eems arg
                            (default: 0.01 )"""
                            )
        parser.add_argument('--qSeedsProposalS2',
                            default=0.10,
                            help="""eems arg
                            (default: 0.1 )"""
                            )
        parser.add_argument('--mEffctProposalS2', '--mEffectProposalS2',
                            default=0.10,
                            help="""eems arg
                            (default: 0.10 )"""
                            )
        parser.add_argument('--qEffctProposalS2', '--qEffectProposalS2',
                            default=0.001,
                            help="""eems arg
                            (default: 0.001 )"""
                            )
        parser.add_argument('--mrateMuProposalS2',
                            default=0.01,
                            help="""eems arg
                            (default: 0.01 )"""
                            )
        parser.add_argument('--saveMatrices',
                            default=0,
                            help="""eems arg
                            (default: 1 )"""
                            )
        parser.add_argument('--numOutputIter',
                            default=10,
                            help="""eems arg
                            (default: 10 )"""
                            )
        parser.add_argument('--prev', '--prevpath',
                            default='',
                            help="""eems arg
                            (default: '' )"""
                            )

    @staticmethod
    def create_parser_map(parser):
        parser.add_argument('--polygon',
                            default=None,
                            help="""A file with the polygon describing the region to
                            run eems on.
                            """)
        parser.add_argument('--wrap', '--wrap_america',
                            default=True,
                            help="""Should all coordinates be wrapped s.t. the
                            americas
                            appear in the east?
                            """)
        parser.add_argument('--region',
                            nargs="*",
                            default=None,
                            action='append',
                            help="""A set of continents, regions or countries
                            that should be included in the analysis. Default:
                            None
                            """)
        parser.add_argument('--population',
                            nargs="*",
                            default=None,
                            action='append',
                            help="""A set of populations that will be retained
                            """)
        parser.add_argument('--hull', '--convex-hull', '--convex_hull',
                            default=False,
                            action='store_true',
                            help="""should a convex hull around the samples
                            be computed? If yes, an intersection of the
                            samples and their continent is used.
                            """)
        parser.add_argument('--envelope',
                            default=False,
                            action='store_true',
                            help="""should an envelop (bounding box) around
                            the samples be computed? If yes, the inference
                            area is restricted to that bounding box.
                            """)
        parser.add_argument('--region-buffer', '--region_buffer',
                            default=1,
                            type=float,
                            help="""how much space should there be between 
                            borders/oceans and the boundary of the eems surface.
                            Currently, this is given in lat/longitude units
                            for simplicity (default 1)
                            """)
        parser.add_argument('--sample-buffer', '--sample_buffer',
                            default=1.,
                            type=float,
                            help="""how much space should there be between the
                            samples and the boundary of the eems surface.
                            Currently, this is given in lat/longitude units
                            for simplicity (default 1)
                            """)
        parser.add_argument('--map-projection',
                            default=None,
                            help="""should the coordinates of samples be
                            changed according to some map-projection? See
                            plt_toolkits.Basemap for a list of all
                            possible projections.
                            """)

        s = 'maps/ne_10m_admin_0_map_subunits.shp'
        parser.add_argument('--map',
                            default=os.path.join(os.path.dirname(__file__), s),
                            help="""what map file should be loaded. Expects a
                            shapefile *.shp/*.shx combo of different countries.
                            The default is %s, which was downloaded from
                            http://www.naturalearthdata.com/downloads/
                            """ % s)


    @staticmethod
    def create_parser_files(parser):
        parser.add_argument('--bed', '--bfile',
                            help="The common name of the bed file to be used")
        parser.add_argument('--diffs', default=None,
                            help='''A diffs file from a previous bed2diffs run,
                            without extension. If not None, the diffs file is
                            filtered rather than a new diffs file created from the
                            bed file.''')
    
        parser.add_argument('--loc', default=None,
                            help=""" File with location information.
                            Should have a column named `pop` and columns named
                            `latitude` and `longitude` or a variation thereof.""")
        parser.add_argument('--loc-has-no-header', 
                            action='store_false', dest="location_header", help="""add this flag if the
                            location file (--loc) doesn't have a header line. In
                            this case, the first three columns are assumed to be
                            the
                            population id, latitude and longitude, respectively."""
                            )
        parser.add_argument('--loc-has-header', default=True,
                            action='store_true', dest="location_header", help="""add this flag if the
                            location file (--loc) does have a header line. In
                            this case, the first three columns are assumed to be
                            the
                            population id, latitude and longitude, respectively."""
                            )
    
        parser.add_argument('--sample-has-no-header', 
                            action='store_false', dest="sample_header", help="""add this flag if the
                            sample file (--sample) doesn't have a header line. In
                            this case, the first three columns are assumed to be
                            the
                            sample id and population id , respectively."""
                            )
        parser.add_argument('--sample-has-header', default=True,
                            action='store_true', dest="sample_header", help="""add this flag if the
                            sample file (--sample) does have a header line. In
                            this case, the first three columns are assumed to be
                            the
                            sample id and population id, latitude and longitude, respectively."""
                            )
        parser.add_argument('--sample', default=None,
                            help=""" File with sample information.
                            Should have a column named `sample` and columns named
                            `pop` or a variation thereof.""")
    
        parser.add_argument('--ind', default=None,
                            help=""" File with individual based 
                            location information.
                            Should have a column named `sample` and columns named
                            `latitude` and `longitude` or a variation thereof.""")
        parser.add_argument('--ind-has-no-header', 
                            action='store_false', dest="ind_header", help="""add this flag if the
                            individual file (--ind) doesn't have a header line. In
                            this case, the first three columns are assumed to be
                            the
                            individual id, latitude and longitude, respectively."""
                            )
        parser.add_argument('--ind-has-header', default=True,
                            action='store_true', dest="ind_header", help="""add this flag if the
                            ind file (--ind) does have a header line."""
                            )

        parser.add_argument('--sd', default=None,
                            help=""" File with individual based
                            sd information.
                            Should have a column named `sample` and
                            columns named `sd.""")
        parser.add_argument('--has-dataset', default=False,
                            action='store_true',
                            help=""" Whether there  is a dataset column
                            that will be passed to meta
                            """)
        parser.add_argument('--output-prefix', default='TMP__PLINK',
                            dest='plinkfile',
                            help="""The plink prefix of the subsetted data
                            set that will be created
                            """)

    @staticmethod
    def create_parser_further_args(parser):
        parser.add_argument('--dry', default=False, action='store_true',
                            help="if set, files are created, but eems is not ran")
        parser.add_argument('--n_runs', '--nruns', '--n-runs',
                            default=1, help="""the number of independendt eems
                            runs to be started. (default 1)""")
        parser.add_argument('--run_script', '--run-script',
                            default=False, action='store_true',
                            help="""should a run submit script be generated?
                            """)
        parser.add_argument('--submit_script', '--submit-script',
                            default=False, action='store_true',
                            help="""should a submit script be generated?
                            """)
        parser.add_argument('--max-missing',
                            default=0.001, type=float,
                            help="""maximum number of missing
                            data that is allowed for loci to be included
                            (default 0.001)""")

    @staticmethod
    def create_parser_folders(parser):
        parser.add_argument('--plink',
                            default="plink",
                            help="The path of your plink exe")
        parser.add_argument('--eems', '--eems-folder',
                            default="/data/eems-project/eems/",
                            help="The base folder of your local eems installation")
        parser.add_argument('--bed2diffs',
                            default=None,
                            help="""The bed2diffs executable, defaults to
                            bed2diffs/bed2diffs in the directory of --eems""")
        parser.add_argument('--eems_snps',
                            default=None,
                            help="""The eems_snps executable, defaults to
                            runeems_snps/runeems_snps in the directory of --eems"""
                            )
        parser.add_argument('--input-folder', '--input_folder',
                            default=None,
                            help="""the folder where all eems input files will
                            be stored. (default: ./input )"""
                            )
        parser.add_argument('--output-folder', '--output_folder',
                            default=None,
                            help="""the folder where all eems output files will
                            be stored. (default: ./output )"""
                            )
        parser.add_argument('--tmp-folder', '--tmp_folder',
                            default=None,
                            help="""the folder where tempory output files will
                            be stored. (default: ./tmp )"""
                            )
        parser.add_argument('--analysis-folder', '--analysis_folder',
                            default='./',
                            help="""the folder where all analysis will be stored
                             (default: . )"""
                            )
        parser.add_argument('--data-folder', '--data_folder',
                            default=".",
                            help="""the folder where all data files are read from
                            (default: . )"""
                            )
        parser.add_argument('--proj', '--proj-name', '--proj_name',
                            default='eems_proj',
                            help="""The name of the output files""")

    @staticmethod
    def create_parser():
        """
        generates ArgumentParser and reads options from CLI

        use -h flag for details
        """

        if hasattr(Parameters, "parser"):
            return
        parser = argparse.ArgumentParser("eems_pipeline",
                                         fromfile_prefix_chars='@')
        
        parser_files = parser.add_argument_group('input files')
        Parameters.create_parser_files(parser_files)

        parser_map = parser.add_argument_group('map options',
                       """ These options control in what space the eems
                        algorithm is run. There are four basic options,
                        if all are set we use the intersection.
                       """)
        Parameters.create_parser_map(parser_map)

        parser_folders = parser.add_argument_group('input/output folders')
        Parameters.create_parser_folders(parser_folders)

        parser_eems = parser.add_argument_group('eems runtime options')
        Parameters.create_parser_eems(parser_eems)

        parser_further = parser.add_argument_group('further options')
        Parameters.create_parser_further_args(parser_further)

        Parameters.parser = parser

    @staticmethod
    def from_command_line():
        """loads arguments from command line
        
        Returns
        -------
        p : Parameters
            the parameters object read from the command line
        """

        Parameters.create_parser()
        parser = Parameters.parser
        params = parser.parse_args()

        p = Parameters(**params.__dict__)
        p.postprocess_args()
        return p

    def postprocess_args(p):
        """
        processes some args in p
        """
        if p.region is not None:
            if type(p.region[0]) is list:
                p.region = [item for sublist in p.region 
                            for item in sublist]

        if p.population is not None:
            if type(p.population[0]) is list:
                p.population = [item for sublist in p.population 
                            for item in sublist]

        p.eems_args = dict()
        p.eems_args['diploid'] = p.diploid.lower()
        p.eems_args['numMCMCIter'] = p.numMCMCIter
        p.eems_args['numBurnIter'] = p.numBurnIter
        p.eems_args['numThinIter'] = p.numThinIter
        p.eems_args['nDemes'] = p.nDemes
        p.eems_args['negBiSize'] = p.negBiSize
        p.eems_args['negBiProb'] = p.negBiProb
        p.eems_args['negBiSize'] = p.negBiSize
        p.eems_args['mrateShape'] = p.mrateShape
        p.eems_args['qrateShape'] = p.qrateShape
        p.eems_args['s2locShape'] = p.s2locShape
        p.eems_args['mrateScale'] = p.mrateScale
        p.eems_args['qrateScale'] = p.qrateScale
        p.eems_args['s2rateScale'] = p.s2rateScale
        p.eems_args['mSeedsProposalS2'] = p.mSeedsProposalS2
        p.eems_args['qSeedsProposalS2'] = p.qSeedsProposalS2
        p.eems_args['qEffctProposalS2'] = p.qEffctProposalS2
        p.eems_args['mEffctProposalS2'] = p.mEffctProposalS2
        p.eems_args['mrateMuProposalS2'] = p.mrateMuProposalS2
        p.eems_args['saveMatrices'] = p.saveMatrices
        p.eems_args['numOutputIter'] = p.numOutputIter
        p.eems_args['prevpath'] = p.prev

        make_full_paths(p)

        if p.eems_snps is None:
            p.eems_snps = "%s/runeems_snps/src/runeems_snps" % p.eems
        if p.bed2diffs is None:
            p.bed2diffs = "%s/bed2diffs/bed2diffs" % p.eems
