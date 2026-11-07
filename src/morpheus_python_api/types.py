"""types.py
Module for any type and enum definitions useful across modules.
"""

from dataclasses import dataclass
from enum import auto, Enum, StrEnum
from pydantic import BaseModel, ConfigDict


class Language(Enum):
    GREEK = auto()
    LATIN = auto()
    ITALIAN = auto()


class CrunchOptions(BaseModel):
    model_config = ConfigDict(extra="forbid")
    language: Language = Language.GREEK
    non_strict_case: bool = False
    ignore_accents: bool = False
    database_format: bool = False
    ending_index: bool = False
    keep_beta_code: bool = False
    lemma: bool = False
    perseus_format_off: bool = False
    verbs_only: bool = False
    raise_on_failure: bool = True


# Cruncher doesn't actually use all of these
# This project's structured parsing DOES use
# ADV, but cruncher itself doesn't
class POS(StrEnum):
    NOUN = "noun"
    VERB = "verb"
    ADJ = "adj"  # adjective
    ADV = "adv"  # adverb
    PREP = "prep"  # preposition
    PRON = "pron"  # pronoun
    CONJ = "conj"  # conjunction
    PART = "part"  # participle


class Case(StrEnum):
    NOM = "nom"  # nominative
    GEN = "gen"  # genitive
    DAT = "dat"  # dative
    ACC = "acc"  # accusative
    VOC = "voc"  # vocative
    ABL = "abl"  # ablative


class Num(StrEnum):
    SG = "sg"  # singular
    PL = "pl"  # plural
    DUAL = "dual"  # dual


class Gender(StrEnum):
    MASC = "masc"  # masculine
    FEM = "fem"  # feminine
    NEUT = "neut"  # neuter


class Tense(StrEnum):
    PRES = "pres"  # present
    IMPERF = "imperf"  # imperfect
    FUT = "fut"  # future
    AOR = "aor"  # aorist
    PERF = "perf"  # perfect
    PLUP = "plup"  # pluperfect
    FUTPERF = "futperf"  # future perfect
    SUPINE = "supine"  # also for tense
    GERUNDIVE = "gerundive"  # Latin/Italian, also in tense
    PASTABS = "pastabs"  # Italian passato remoto


class Mood(StrEnum):
    IND = "ind"  # indicative
    SUBJ = "subj"  # subjunctive
    OPT = "opt"  # optative
    IMPERAT = "imperat"  # imperative
    INF = "inf"  # infinitive
    PART = "part"  # participle
    SUPINE = "supine"  # Latin, also tense
    GERUNDIVE = "gerundive"  # Latin/Italian, also tense
    COND = "cond"  # Italian conditional


class Voice(StrEnum):
    ACT = "act"  # active
    MID = "mid"  # middle
    PASS = "pass"  # passive
    MP = "mp"  # medio-passive


class Person(StrEnum):
    FIRST = "first"
    SECOND = "second"
    THIRD = "third"


class Degree(StrEnum):
    COMP = "comp"
    SUPERL = "superl"


# Note that Latin always has no specified dialects
# and that morphkeys.h also accepts non_homeric_epic and ionic/homeric,
# but these aren't actually produced by any cruncher parse
class Dialect(StrEnum):
    AEOLIC = "aeolic"
    ATTIC = "attic"
    DORIC = "doric"
    EPIC = "epic"
    HOMERIC = "homeric"
    IONIC = "ionic"
    PARAD_FORM = "parad_form"  # PARADIGMATIC FORM
    PROSE = "prose"


# BEGIN: code generated with Claude Sonnet 5.5


class StemType(StrEnum):
    """Stem types, Greek and Latin combined."""

    ZERO_A_UM = "0_a_um"
    ZERO_ADJ3 = "0_adj3"
    ZERO_I = "0_i"
    ZERO_IS = "0_is"
    A_ACC = "a_acc"
    A_AE = "a_ae"
    A_E = "a_e"
    A_HS = "a_hs"
    ADVERB = "adverb"
    AH_AHS = "ah_ahs"
    AJW_PR = "ajw_pr"
    ALPHABETIC = "alphabetic"
    AMI_AOR = "ami_aor"
    AMI_PR = "ami_pr"
    AMI_SHORT = "ami_short"
    AN_ALNIS = "an_aLnis"
    ANS_ADJ = "ans_adj"
    ANS_ANTIS = "ans_antis"
    AOR1 = "aor1"
    AOR2 = "aor2"
    AOR2_PASS = "aor2_pass"
    AOR_PASS = "aor_pass"
    AOS_AOU = "aos_aou"
    AR_ATOS = "ar_atos"
    ART_ADJ = "art_adj"
    ARTICLE = "article"
    AS_A = "as_a"
    AS_ADIS = "as_adis"
    AS_AE = "as_ae"
    AS_AINA_AN = "as_aina_an"
    AS_ANTIS = "as_antis"
    AS_ANTOS = "as_antos"
    AS_AOS = "as_aos"
    AS_ASA_AN = "as_asa_an"
    AS_ATOS = "as_atos"
    ATH_H_AOR = "ath_h_aor"
    ATH_PRIMARY = "ath_primary"
    ATH_SECONDARY = "ath_secondary"
    ATH_U_AOR = "ath_u_aor"
    ATH_W_AOR = "ath_w_aor"
    AVPERF = "avperf"
    AW_FUT = "aw_fut"
    AW_PR = "aw_pr"
    AX_ADJ = "ax_adj"
    C_GGOS = "c_ggos"
    C_GOS = "c_gos"
    C_KOS = "c_kos"
    C_KTOS = "c_ktos"
    C_XOS = "c_xos"
    CO_CA = "co_ca"
    CONJ = "conj"
    CONJ1 = "conj1"
    CONJ1_C = "conj1_c"
    CONJ1_CI = "conj1_ci"
    CONJ1_G = "conj1_g"
    CONJ1_GI = "conj1_gi"
    CONJ2 = "conj2"
    CONJ3 = "conj3"
    CONJ3_IO = "conj3_io"
    CONJ4 = "conj4"
    CONJ_A = "conj_a"
    CONJ_O = "conj_o"
    CONJ_U = "conj_u"
    DEMONSTR = "demonstr"
    ELR_ELRIS = "eLr_eLris"
    ELS_ERIS = "eLs_eris"
    E_ES = "e_es"
    E_I = "e_i"
    EH_EHS = "eh_ehs"
    EHS_EOU = "ehs_eou"
    EIS_ENOS = "eis_enos"
    EIS_ESSA = "eis_essa"
    EMI_AOR = "emi_aor"
    EMI_PR = "emi_pr"
    EN_INIS = "en_inis"
    ENS_ADJ = "ens_adj"
    ENS_ENTIS = "ens_entis"
    EOS_EH_EON = "eos_eh_eon"
    EOS_EOU = "eos_eou"
    EPS_IPIS = "eps_ipis"
    EPS_IPITIS = "eps_ipitis"
    ER_ERA_ERUM = "er_era_erum"
    ER_ERIS = "er_eris"
    ER_RA_RUM = "er_ra_rum"
    ER_RI = "er_ri"
    ER_RIS = "er_ris"
    ER_RIS_RE = "er_ris_re"
    ES_AE = "es_ae"
    ES_ELDIS = "es_eLdis"
    ES_ELI = "es_eLi"
    ES_ELTIS = "es_eLtis"
    ES_EI = "es_ei"
    ES_IS = "es_is"
    ES_ITIS = "es_itis"
    EUS_EI = "eus_ei"
    EUS_EWS = "eus_ews"
    EVPERF = "evperf"
    EVW_PR = "evw_pr"
    EW_FUT = "ew_fut"
    EW_PR = "ew_pr"
    EX_ICIS = "ex_icis"
    EX_ICIS_ADJ = "ex_icis_adj"
    EX_IGIS = "ex_igis"
    EXCLAM = "exclam"
    EXPLETIVE = "expletive"
    FUT_PERF = "fut_perf"
    GC_GOS = "gc_gos"
    GO_GA = "go_ga"
    H_HS = "h_hs"
    HC_EKOS = "hc_ekos"
    HEIS_HESSA = "heis_hessa"
    HN_ENOS = "hn_enos"
    HR_EROS = "hr_eros"
    HS_EOS = "hs_eos"
    HS_ES = "hs_es"
    HS_OU = "hs_ou"
    INDECL = "indecl"
    INDECL_NOUN = "indecl_noun"
    INDEF = "indef"
    INTERROG = "interrog"
    IO_I = "io_i"
    IOR_IUS_COMP = "ior_ius_comp"
    IOS_I = "ios_i"
    IRREG_ADJ1 = "irreg_adj1"
    IRREG_ADJ3 = "irreg_adj3"
    IRREG_DECL3 = "irreg_decl3"
    IRREG_MI = "irreg_mi"
    IRREG_NOM = "irreg_nom"
    IRREG_NOM2 = "irreg_nom2"
    IRREG_NOM3 = "irreg_nom3"
    IRREG_PP1 = "irreg_pp1"
    IS_E = "is_e"
    IS_EOS = "is_eos"
    IS_ERIS = "is_eris"
    IS_EWS = "is_ews"
    IS_ICDOS = "is_iCdos"
    IS_IDIS = "is_idis"
    IS_IDOS = "is_idos"
    IS_IDOS_ADJ = "is_idos_adj"
    IS_IS = "is_is"
    IS_IS_C = "is_is_C"
    IS_ITOS = "is_itos"
    IUS_I = "ius_i"
    IUS_IA_IUM = "ius_ia_ium"
    IVPERF = "ivperf"
    IX_ADJ = "ix_adj"
    IX_ILCIS = "ix_iLcis"
    IX_ICIS = "ix_icis"
    KLEHS_KLEOUS = "klehs_kleous"
    MA_MATIS = "ma_matis"
    MA_MATOS = "ma_matos"
    MEN_MINIS = "men_minis"
    N_NOS = "n_nos"
    N_NTOS = "n_ntos"
    NUMERAL = "numeral"
    OLN_OLNIS = "oLn_oLnis"
    OLN_ONIS = "oLn_onis"
    O_A = "o_a"
    O_ELNIS = "o_eLnis"
    O_I = "o_i"
    O_INIS = "o_inis"
    O_OLNIS = "o_oLnis"
    O_ONIS = "o_onis"
    O_US = "o_us"
    OEIS_OENTOS = "oeis_oentos"
    OEIS_OESSA = "oeis_oessa"
    OMI_AOR = "omi_aor"
    OMI_PR = "omi_pr"
    ON_ONTIS = "on_ontis"
    OOS_OH_OON = "oos_oh_oon"
    OOS_OON = "oos_oon"
    OOS_OOU = "oos_oou"
    OR_OLRIS = "or_oLris"
    OR_ORIS = "or_oris"
    OR_US_COMP = "or_us_comp"
    OS_H_ON = "os_h_on"
    OS_I = "os_i"
    OS_OIS = "os_ois"
    OS_ON = "os_on"
    OS_OU = "os_ou"
    OUS_ONTOS = "ous_ontos"
    OW_PR = "ow_pr"
    OX_ADJ = "ox_adj"
    PARTICLE = "particle"
    PELS_PEDIS = "peLs_pedis"
    PELS_PEDIS_ADJ = "peLs_pedis_adj"
    PERF2_ACT = "perf2_act"
    PERF_ACT = "perf_act"
    PERFP_D = "perfp_d"
    PERFP_G = "perfp_g"
    PERFP_L = "perfp_l"
    PERFP_N = "perfp_n"
    PERFP_P = "perfp_p"
    PERFP_R = "perfp_r"
    PERFP_S = "perfp_s"
    PERFP_VOW = "perfp_vow"
    PERFSTEM = "perfstem"
    POUS_PODOS = "pous_podos"
    PP4 = "pp4"
    PREP = "prep"
    PRON1 = "pron1"
    PRON2 = "pron2"
    PRON3 = "pron3"
    PRON_ADJ1 = "pron_adj1"
    PRON_ADJ3 = "pron_adj3"
    QRIC_TRIXOS = "qric_trixos"
    R_ROS = "r_ros"
    R_RTOS = "r_rtos"
    REG_FUT = "reg_fut"
    RELATIVE = "relative"
    S_DIS = "s_dis"
    S_DOS = "s_dos"
    S_IS = "s_is"
    S_NIS = "s_nis"
    S_NOS = "s_nos"
    S_NTOS = "s_ntos"
    S_OS = "s_os"
    S_QOS = "s_qos"
    S_ROS = "s_ros"
    S_TIS = "s_tis"
    S_TIS_ADJ = "s_tis_adj"
    S_TOS = "s_tos"
    T_TOS = "t_tos"
    TAS_TATIS = "tas_tatis"
    ULS_ULRIS = "uLs_uLris"
    ULS_UOS = "uLs_uos"
    U_ACC = "u_acc"
    UMI_PR = "umi_pr"
    UNS_UNTIS = "uns_untis"
    UR_ORIS = "ur_oris"
    US_A_UM = "us_a_um"
    US_EIA_U = "us_eia_u"
    US_ERIS = "us_eris"
    US_EWS = "us_ews"
    US_I = "us_i"
    US_IUS_ADJ = "us_ius_adj"
    US_ORIS = "us_oris"
    US_U = "us_u"
    US_UNTIS = "us_untis"
    US_UOS = "us_uos"
    US_US = "us_us"
    VERB_ADJ1 = "verb_adj1"
    VERB_ADJ2 = "verb_adj2"
    WCN_WCNTOS = "wCn_wCntos"
    W_OOS = "w_oos"
    W_STEM = "w_stem"
    WN_NOS = "wn_nos"
    WN_ON = "wn_on"
    WN_ON_COMP = "wn_on_comp"
    WN_ONOS = "wn_onos"
    WN_ONTOS = "wn_ontos"
    WN_OUSA_ON = "wn_ousa_on"
    WR_OROS = "wr_oros"
    WS_OOS = "ws_oos"
    WS_W = "ws_w"
    WS_W_LONG = "ws_w_long"
    WS_WN = "ws_wn"
    WS_WOS = "ws_wos"
    WW_PR = "ww_pr"
    X_CIS = "x_cis"
    X_CTIS = "x_ctis"
    X_GIS = "x_gis"
    Y_BOS = "y_bos"
    Y_FOS = "y_fos"
    Y_POS = "y_pos"
    YS_YOS = "ys_yos"


class Deriv(StrEnum):
    """Derivation subtypes."""

    AL_STEM = "aL_stem"
    A_STEM = "a_stem"
    AINW = "ainw"
    AIRW = "airw"
    ALLW = "allw"
    ANW = "anw"
    ARE_VB = "are_vb"
    ARRE_VB = "arre_vb"
    ARSI_VB = "arsi_vb"
    AV_STEM = "av_stem"
    AW_DENOM = "aw_denom"
    AZW = "azw"
    CARE_VB = "care_vb"
    CARSI_VB = "carsi_vb"
    CIARE_VB = "ciare_vb"
    CIARSI_VB = "ciarsi_vb"
    E_STEM = "e_stem"
    E_SUPPL = "e_suppl"
    EINW = "einw"
    EIRW = "eirw"
    ELLW = "ellw"
    ERE_VB = "ere_vb"
    ERSI_VB = "ersi_vb"
    EUW = "euw"
    EV_STEM = "ev_stem"
    EW_DENOM = "ew_denom"
    GARE_VB = "gare_vb"
    GARSI_VB = "garsi_vb"
    GIARE_VB = "giare_vb"
    GIARSI_VB = "giarsi_vb"
    IAW_DENOM = "iaw_denom"
    ILLW = "illw"
    INW = "inw"
    IRE_VB = "ire_vb"
    IRSI_VB = "irsi_vb"
    ISKW = "iskw"
    IZW = "izw"
    NDW = "ndw"
    NHMI = "nhmi"
    NUMI = "numi"
    NW = "nw"
    O_STEM = "o_stem"
    ORRE_VB = "orre_vb"
    OW_DENOM = "ow_denom"
    OZW = "ozw"
    PTW = "ptw"
    REG_CONJ = "reg_conj"
    SKW = "skw"
    SS = "ss"
    ULLW = "ullw"
    UNW = "unw"
    URRE_VB = "urre_vb"
    URW = "urw"
    UZW = "uzw"


class Feature(StrEnum):
    """Flags from the third column of cruncher output (Greek and Latin)"""

    # Register
    EARLY = "early"
    LATE = "late"
    LATER = "later"
    POETIC = "poetic"
    RARE = "rare"

    # Augment
    UNAUGMENTED = "unaugmented"
    SYLL_AUGMENT = "syll_augment"
    PREVB_AUG = "prevb_aug"

    # Reduplication
    REDUPL = "redupl"
    ATTIC_REDUPL = "attic_redupl"
    NO_REDUPL = "no_redupl"
    PRES_REDUPL = "pres_redupl"

    # Contraction, elision, and other sound changes
    CONTR = "contr"
    UNCONTR = "uncontr"
    SYNCOPE = "syncope"
    APOCOPE = "apocope"
    DISSIMILATION = "dissimilation"
    DOUBLED_CONS = "doubled_cons"
    ELIDE_PREVERB = "elide_preverb"
    SHORT_EIS = "short_eis"
    SHORT_SUBJ = "short_subj"
    R_E_I_ALPHA = "r_e_i_alpha"
    RAW_SONANT = "raw_sonant"
    N_INFIX = "n_infix"
    IOTA_INTENS = "iota_intens"

    # Clitics
    ENCLITIC = "enclitic"
    PROCLITIC = "proclitic"

    # Movable consonant
    NU_MOVABLE = "nu_movable"

    # Derivational sense
    A_COPUL = "a_copul"  # copulative alpha
    A_PRIV = "a_priv"  # privative alpha
    CAUSAL = "causal"
    DESIDERATIVE = "desiderative"
    DIMINUTIVE = "diminutive"
    FREQUENTAT = "frequentat"  # frequentative
    ITERATIVE = "iterative"

    # Comparison
    COMP_ONLY = "comp_only"
    IRREG_COMP = "irreg_comp"
    IRREG_SUPERL = "irreg_superl"

    # Preverbs
    RAW_PREVERB = "raw_preverb"
    ROOT_PREVERB = "root_preverb"
    UNASP_PREVERB = "unasp_preverb"
    EN_TO_ENI = "en_to_eni"
    META_TO_PEDA = "meta_to_peda"
    PARA_TO_PARAI = "para_to_parai"
    PROS_TO_POTI = "pros_to_poti"
    PROS_TO_PROTI = "pros_to_proti"
    UPO_TO_UPAI = "upo_to_upai"

    # Other
    GEOG_NAME = "geog_name"  # geographical name
    IMPERSONAL = "impersonal"
    INDECLFORM = "indeclform"  # indeclinable form
    INTRANS = "intrans"  # intransitive


# END: code generated with Claude Sonnet 5.5


# NOTE: It's important that field names for these dataclasses be lowercase
# since they're accessed at certainpoints by doing something like
# Tense.__name__.lower()
@dataclass
class MorphParse:
    # Since this class is part of the API
    # we want to store Greek text in utf-8
    # and convert to betacode when needed
    language: Language
    pos: POS
    dict_forms: list[str] | None = None
    # a noun parse can have multiple cases, e.g. nom/voc in cruncher output
    case: frozenset[Case] | None = None
    num: frozenset[Num] | None = None
    gender: frozenset[Gender] | None = None
    tense: frozenset[Tense] | None = None
    mood: frozenset[Mood] | None = None
    voice: frozenset[Voice] | None = None
    person: frozenset[Person] | None = None
    degree: frozenset[Degree] | None = None

    dialect: frozenset[Dialect] | None = None
    features: frozenset[Feature] | None = None
    stem_type: StemType | None = None
    deriv: Deriv | None = None


@dataclass
class WordParse:
    lemma: str
    parses: list[MorphParse]
