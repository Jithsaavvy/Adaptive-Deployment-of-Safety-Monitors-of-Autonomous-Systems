% ===============================================
% Generated code from MiniBrass, do not modify!
include "soft_constraints/mbr_types/probabilistic_type.mzn";
include "soft_constraints/mbr_types/fuzzy_type.mzn";
include "soft_constraints/mbr_types/relation-type.mzn";
include "soft_constraints/mbr_types/bool-type.mzn";
include "soft_constraints/mbr_types/cfn_type.mzn";
include "soft_constraints/mbr_types/weighted_type.mzn";
include "soft_constraints/mbr_types/cr_type.mzn";
include "soft_constraints/mbr_types/free-pvs-type.mzn";

% ---------------------------------------------------
% Overall exported predicate (and objective in case of atomic top-level PVS) : 

% ---------------------------------------------------
function ann:  postGetBetter() = mbr_postGetBetter_cp1();
function ann:  postNotGetWorse() = mbr_postNotGetWorse_cp1();
var set of 1..mbr_nScs_cp1: topLevelObjective;
constraint topLevelObjective = mbr_overall_cp1;

% ---------------------------------------------------
%   PVS cp1
% ---------------------------------------------------
% Parameters: 
int : mbr_nScs_cp1 = 3; 
array[int, 1..2] of 1..mbr_nScs_cp1 : mbr_crEdges_cp1 = [|1, 3 | 2, 3|]; 
bool : mbr_useSPD_cp1 = false; 

% Decision variables: 
var set of 1..mbr_nScs_cp1: mbr_overall_cp1;
array[1..mbr_nScs_cp1] of var bool: mbr_valuations_cp1;
set of 1..mbr_nScs_cp1: mbr_top_cp1 = {};
constraint mbr_overall_cp1 = link_invert_booleans (mbr_valuations_cp1,mbr_nScs_cp1, mbr_crEdges_cp1, mbr_useSPD_cp1);

% MiniSearch predicates: 

% Soft constraints: 
constraint mbr_valuations_cp1[1] = (force_platform[latency] = 20);
constraint mbr_valuations_cp1[2] = (force_platform[latency] = 100);
constraint mbr_valuations_cp1[3] = (force_platform[force_sensor_type] = 4);

function ann: mbr_postGetBetter_cp1() = post(is_worse_cr(sol(mbr_overall_cp1), mbr_overall_cp1, mbr_nScs_cp1, mbr_crEdges_cp1, mbr_useSPD_cp1));

function ann: mbr_postNotGetWorse_cp1() = post(not ( (sol(mbr_overall_cp1) = mbr_overall_cp1) \/ (is_worse_cr(mbr_overall_cp1, sol(mbr_overall_cp1), mbr_nScs_cp1, mbr_crEdges_cp1, mbr_useSPD_cp1))));
output ["force_platform = \(force_platform)"] ++ [ "\nValuations: mbr_overall_cp1 = \(mbr_overall_cp1)\n"];

