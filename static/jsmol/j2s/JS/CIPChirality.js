Clazz.declarePackage ("JS");
Clazz.load (["JU.Lst", "$.V3"], "JS.CIPChirality", ["java.util.Arrays", "$.Hashtable", "JU.BS", "$.Measure", "$.P3", "$.P4", "$.PT", "JU.BSUtil", "$.Logger", "JV.JC"], function () {
c$ = Clazz.decorateAsClass (function () {
this.ptID = 0;
this.root = null;
this.currentRule = 1;
this.lstSmallRings = null;
this.nPriorityMax = 0;
this.bsAtropisomeric = null;
this.bsAromatic = null;
this.bsAzacyclic = null;
this.vNorm = null;
this.vNorm2 = null;
this.vTemp = null;
if (!Clazz.isClassDefined ("JS.CIPChirality.CIPAtom")) {
JS.CIPChirality.$CIPChirality$CIPAtom$ ();
}
Clazz.instantialize (this, arguments);
}, JS, "CIPChirality");
Clazz.prepareFields (c$, function () {
this.lstSmallRings =  new JU.Lst ();
this.vNorm =  new JU.V3 ();
this.vNorm2 =  new JU.V3 ();
this.vTemp =  new JU.V3 ();
});
Clazz.defineMethod (c$, "getRuleName", 
function () {
switch (this.currentRule) {
case 1:
return "1a";
case 2:
return "1b";
default:
return "" + (this.currentRule - 1);
}
});
Clazz.makeConstructor (c$, 
function () {
});
Clazz.defineMethod (c$, "init", 
 function () {
this.ptID = 0;
this.nPriorityMax = 0;
this.lstSmallRings.clear ();
});
Clazz.defineMethod (c$, "getChiralityForAtoms", 
function (atoms, bsAtoms, bsAtropisomeric) {
if (bsAtoms.isEmpty ()) return;
this.bsAtropisomeric = bsAtropisomeric;
this.init ();
var bs = JU.BSUtil.copy (bsAtoms);
while (!bs.isEmpty ()) this.getSmallRings (atoms[bs.nextSetBit (0)], bs);

this.bsAromatic = this.getAromaticity (atoms);
this.bsAzacyclic = this.getAzacyclic (atoms, bsAtoms);
var bsToDo = JU.BSUtil.copy (bsAtoms);
var haveAlkenes = this.preFilterAtomList (atoms, bsToDo);
for (var i = bsToDo.nextSetBit (0); i >= 0; i = bsToDo.nextSetBit (i + 1)) {
var atom = atoms[i];
var c = atom.getCIPChirality (false);
if (c.length > 0) {
bsToDo.clear (i);
} else {
this.ptID = 0;
atom.setCIPChirality (this.getAtomChiralityLimited (atom, null, null, 4));
}}
var lstEZ =  new JU.Lst ();
if (haveAlkenes) {
for (var i = bsToDo.nextSetBit (0); i >= 0; i = bsToDo.nextSetBit (i + 1)) this.getAtomBondChirality (atoms[i], false, 4, lstEZ, bsToDo);

}for (var i = bsToDo.nextSetBit (0); i >= 0; i = bsToDo.nextSetBit (i + 1)) {
var a = atoms[i];
a.setCIPChirality (0);
a.setCIPChirality (this.getAtomChiralityLimited (a, null, null, 6));
}
if (haveAlkenes) {
for (var i = bsToDo.nextSetBit (0); i >= 0; i = bsToDo.nextSetBit (i + 1)) this.getAtomBondChirality (atoms[i], false, 6, lstEZ, bsToDo);

if (this.lstSmallRings.size () > 0 && lstEZ.size () > 0) this.clearSmallRingEZ (atoms, lstEZ);
}}, "~A,JU.BS,JU.BS");
Clazz.defineMethod (c$, "getAzacyclic", 
 function (atoms, bsAtoms) {
var bsAza = null;
for (var i = bsAtoms.nextSetBit (0); i >= 0; i = bsAtoms.nextSetBit (i + 1)) {
var atom = atoms[i];
if (atom.getElementNumber () != 7 || atom.getCovalentBondCount () != 3 || this.bsAromatic != null && this.bsAromatic.get (i)) continue;
var nr = 0;
for (var j = this.lstSmallRings.size (); --j >= 0; ) {
var bsRing = this.lstSmallRings.get (j);
if (bsRing.get (i)) nr++;
}
if (nr != 3) continue;
if (bsAza == null) bsAza =  new JU.BS ();
bsAza.set (i);
}
return bsAza;
}, "~A,JU.BS");
Clazz.defineMethod (c$, "preFilterAtomList", 
 function (atoms, bsToDo) {
var haveAlkenes = false;
for (var i = bsToDo.nextSetBit (0); i >= 0; i = bsToDo.nextSetBit (i + 1)) {
if (!this.couldBeChiralAtom (atoms[i])) {
bsToDo.clear (i);
continue;
}if (!haveAlkenes && this.couldBeChiralAlkene (atoms[i], null) != -1) haveAlkenes = true;
}
return haveAlkenes;
}, "~A,JU.BS");
Clazz.defineMethod (c$, "couldBeChiralAtom", 
 function (a) {
var mustBePlanar = false;
switch (a.getCovalentBondCount ()) {
default:
System.out.println ("???? too many bonds! " + a);
return false;
case 0:
return false;
case 1:
return false;
case 2:
return a.getElementNumber () == 7;
case 3:
switch (a.getElementNumber ()) {
case 7:
if (this.bsAzacyclic != null && this.bsAzacyclic.get (a.getIndex ())) break;
return false;
case 6:
mustBePlanar = true;
break;
case 15:
case 16:
case 33:
case 34:
case 51:
case 52:
case 83:
case 84:
break;
case 4:
break;
default:
return false;
}
break;
case 4:
break;
}
var edges = a.getEdges ();
var nH = 0;
for (var j = a.getBondCount (); --j >= 0; ) {
if (edges[j].getOtherAtomNode (a).getAtomicAndIsotopeNumber () == 1 && ++nH == 2) {
return false;
}}
var d = this.getTrigonality (a, this.vNorm);
var planar = (Math.abs (d) < 0.2);
if (planar == mustBePlanar) return true;
System.out.println ("??????? planar=" + planar + "??" + a);
return false;
}, "JU.Node");
Clazz.defineMethod (c$, "couldBeChiralAlkene", 
 function (a, b) {
switch (a.getCovalentBondCount ()) {
default:
return -1;
case 2:
if (a.getElementNumber () != 7) return -1;
break;
case 3:
if (!this.isFirstRow (a)) return -1;
break;
}
var bonds = a.getEdges ();
var n = 0;
for (var i = bonds.length; --i >= 0; ) if (bonds[i].getCovalentOrder () == 2) {
if (++n > 1) return -3;
var other = bonds[i].getOtherAtomNode (a);
if (!this.isFirstRow (other)) return -1;
if (b != null && (other !== b || b.getCovalentBondCount () == 1)) {
return -1;
}}
return -2;
}, "JU.Node,JU.Node");
Clazz.defineMethod (c$, "isFirstRow", 
function (a) {
var n = a.getElementNumber ();
return (n > 2 && n <= 10);
}, "JU.Node");
Clazz.defineMethod (c$, "getSmallRings", 
 function (atom, bs) {
this.lstSmallRings =  new JU.Lst ();
this.root = Clazz.innerTypeInstance (JS.CIPChirality.CIPAtom, this, null).create (atom, null, false, false);
this.addSmallRings (this.root, bs);
}, "JU.Node,JU.BS");
Clazz.defineMethod (c$, "getAromaticity", 
 function (atoms) {
var bsAromatic =  new JU.BS ();
for (var i = this.lstSmallRings.size (); --i >= 0; ) {
var bsRing = this.lstSmallRings.get (i);
var isAromatic = true;
for (var j = bsRing.nextSetBit (0); j >= 0; j = bsRing.nextSetBit (j + 1)) {
switch (atoms[j].getCovalentBondCount ()) {
case 2:
case 3:
continue;
default:
isAromatic = false;
break;
}
}
if (isAromatic) bsAromatic.or (bsRing);
}
return (bsAromatic.isEmpty () ? null : bsAromatic);
}, "~A");
Clazz.defineMethod (c$, "addSmallRings", 
 function (a, bs) {
if (a == null || a.atom == null) return;
if (bs != null) bs.clear (a.atom.getIndex ());
if (a.isTerminal || a.isDuplicate || a.atom.getCovalentBondCount () > 4) return;
var bonds = a.atom.getEdges ();
var atom2;
var pt = 0;
for (var i = bonds.length; --i >= 0; ) {
var bond = bonds[i];
if (bond == null || !bond.isCovalent () || (atom2 = bond.getOtherAtomNode (a.atom)).getCovalentBondCount () == 1 || a.parent != null && atom2 === a.parent.atom) continue;
var r = a.addAtom (pt++, atom2, false, false);
if (r.isRingDuplicate) r.updateRingList ();
}
for (var i = 0; i < pt; i++) {
this.addSmallRings (a.atoms[i], bs);
}
}, "JS.CIPChirality.CIPAtom,JU.BS");
Clazz.defineMethod (c$, "clearSmallRingEZ", 
 function (atoms, lstEZ) {
for (var j = this.lstSmallRings.size (); --j >= 0; ) this.lstSmallRings.get (j).andNot (this.bsAtropisomeric);

for (var i = lstEZ.size (); --i >= 0; ) {
var ab = lstEZ.get (i);
for (var j = this.lstSmallRings.size (); --j >= 0; ) {
var ring = this.lstSmallRings.get (j);
if (ring.get (ab[0]) && ring.get (ab[1])) {
atoms[ab[0]].setCIPChirality (3);
atoms[ab[1]].setCIPChirality (3);
}}
}
}, "~A,JU.Lst");
Clazz.defineMethod (c$, "getTrigonality", 
function (a, vNorm) {
var pts =  new Array (3);
var bonds = a.getEdges ();
for (var i = bonds.length, pt = 0; --i >= 0 && pt < 3; ) if (bonds[i].isCovalent ()) pts[pt++] = bonds[i].getOtherAtomNode (a).getXYZ ();

var plane = JU.Measure.getPlaneThroughPoints (pts[0], pts[1], pts[2], vNorm, this.vTemp,  new JU.P4 ());
return JU.Measure.distanceToPlane (plane, a.getXYZ ());
}, "JU.Node,JU.V3");
Clazz.defineMethod (c$, "getAtomChirality", 
function (atom) {
this.init ();
return this.getAtomChiralityLimited (atom, null, null, 4);
}, "JU.Node");
Clazz.defineMethod (c$, "getBondChirality", 
function (bond) {
this.init ();
this.getSmallRings (bond.getOtherAtomNode (null), null);
return (bond.getCovalentOrder () == 2 ? this.getBondChiralityLimited (bond, null, 4) : 0);
}, "JU.Edge");
Clazz.defineMethod (c$, "getAtomBondChirality", 
 function (atom, allBonds, ruleMax, lstEZ, bsToDo) {
var index = atom.getIndex ();
var bonds = atom.getEdges ();
var c = 0;
var isAtropic = this.bsAtropisomeric.get (index);
for (var j = bonds.length; --j >= 0; ) {
var bond = bonds[j];
var atom1;
var index1;
if (isAtropic) {
atom1 = bonds[j].getOtherAtomNode (atom);
index1 = atom1.getIndex ();
if (!this.bsAtropisomeric.get (index1)) continue;
c = this.getAxialOrEZChirality (atom, atom1, atom, atom1, true, ruleMax);
} else if (bond.getCovalentOrder () == 2) {
atom1 = this.getLastCumuleneAtom (bond, atom, null, null);
index1 = atom1.getIndex ();
if (!allBonds && index1 < index) continue;
c = this.getBondChiralityLimited (bond, atom, ruleMax);
} else {
continue;
}if (c != 0) {
if (!isAtropic) lstEZ.addLast ( Clazz.newIntArray (-1, [index, index1]));
bsToDo.clear (index);
bsToDo.clear (index1);
}if (isAtropic) break;
}
}, "JU.Node,~B,~N,JU.Lst,JU.BS");
Clazz.defineMethod (c$, "getLastCumuleneAtom", 
 function (bond, atom, nSP2, parents) {
var atom2 = bond.getOtherAtomNode (atom);
if (parents != null) {
parents[0] = atom2;
parents[1] = atom;
}if (nSP2 != null) nSP2[0] = 2;
var ppt = 0;
while (true) {
if (atom2.getCovalentBondCount () != 2) return atom2;
var edges = atom2.getEdges ();
for (var i = edges.length; --i >= 0; ) {
var atom3 = (bond = edges[i]).getOtherAtomNode (atom2);
if (atom3 === atom) continue;
if (bond.getCovalentOrder () != 2) return atom2;
if (parents != null) {
if (ppt == 0) {
parents[0] = atom2;
ppt = 1;
}parents[1] = atom2;
}if (nSP2 != null) nSP2[0]++;
atom = atom2;
atom2 = atom3;
break;
}
}
}, "JU.Edge,JU.Node,~A,~A");
Clazz.defineMethod (c$, "getAtomChiralityLimited", 
 function (atom, cipAtom, parent, ruleMax) {
var rs = 0;
var isChiral = false;
var isAlkene = false;
try {
if (cipAtom == null) {
cipAtom = Clazz.innerTypeInstance (JS.CIPChirality.CIPAtom, this, null).create (atom, null, false, isAlkene);
var nSubs = atom.getCovalentBondCount ();
var elemNo = atom.getElementNumber ();
isAlkene = (nSubs == 3 && elemNo <= 10 && cipAtom.lonePair == null);
if (nSubs != (parent == null ? 4 : 3) - (nSubs == 3 && !isAlkene ? 1 : 0)) return rs;
} else {
atom = cipAtom.atom;
isAlkene = cipAtom.isAlkene;
}this.root = cipAtom;
cipAtom.parent = parent;
if (parent != null) cipAtom.htPathPoints = parent.htPathPoints;
this.currentRule = 1;
if (cipAtom.set ()) {
for (this.currentRule = 1; this.currentRule <= ruleMax; this.currentRule++) {
if (JU.Logger.debugging) JU.Logger.info ("-Rule " + this.getRuleName () + " CIPChirality for " + cipAtom + "-----");
if (this.currentRule == 5) {
cipAtom.createAuxiliaryRSCenters (null, null);
}isChiral = false;
cipAtom.sortSubstituents ();
isChiral = true;
if (JU.Logger.debugging) {
JU.Logger.info (this.currentRule + ">>>>" + cipAtom);
for (var i = 0; i < cipAtom.bondCount; i++) {
if (cipAtom.atoms[i] != null) JU.Logger.info (cipAtom.atoms[i] + " " + Integer.toHexString (cipAtom.prevPriorities[i]));
}
}if (cipAtom.achiral) {
isChiral = false;
break;
}for (var i = 0; i < cipAtom.bondCount - 1; i++) {
if (cipAtom.prevPriorities[i] == cipAtom.prevPriorities[i + 1]) {
isChiral = false;
break;
}}
if (this.currentRule == 6) cipAtom.isPseudo = cipAtom.canBePseudo;
if (isChiral) {
rs = (!isAlkene ? cipAtom.checkHandedness () : cipAtom.atoms[0].isDuplicate ? 2 : 1);
if (!isAlkene && cipAtom.isPseudo && cipAtom.canBePseudo) rs = rs | 4;
break;
}}
if (JU.Logger.debugging) JU.Logger.info (atom + " " + rs + "\n----------------------------------");
}} catch (e) {
System.out.println (e + " in CIPChirality");
{
alert(e);
}return 3;
}
return rs;
}, "JU.Node,JS.CIPChirality.CIPAtom,JS.CIPChirality.CIPAtom,~N");
Clazz.defineMethod (c$, "getBondChiralityLimited", 
 function (bond, a, ruleMax) {
if (JU.Logger.debugging) JU.Logger.info ("get Bond Chirality " + bond);
if (a == null) a = bond.getOtherAtomNode (null);
var b = bond.getOtherAtomNode (a);
if (this.couldBeChiralAlkene (a, b) == -1) return 0;
var nSP2 =  Clazz.newIntArray (1, 0);
var parents =  new Array (2);
b = this.getLastCumuleneAtom (bond, a, nSP2, parents);
var isCumulene = (nSP2[0] > 2);
var isAxial = isCumulene && (nSP2[0] % 2 == 1);
return this.getAxialOrEZChirality (a, parents[0], parents[1], b, isAxial, ruleMax);
}, "JU.Edge,JU.Node,~N");
Clazz.defineMethod (c$, "getAxialOrEZChirality", 
 function (a, pa, pb, b, isAxial, ruleMax) {
var a1 = Clazz.innerTypeInstance (JS.CIPChirality.CIPAtom, this, null).create (a, null, false, true);
var b1 = Clazz.innerTypeInstance (JS.CIPChirality.CIPAtom, this, null).create (pa, null, false, true);
a1.canBePseudo = a1.isOddCumulene = isAxial;
var atop = this.getAtomChiralityLimited (a, a1, b1, ruleMax) - 1;
var a2 = Clazz.innerTypeInstance (JS.CIPChirality.CIPAtom, this, null).create (pb, null, false, true);
var b2 = Clazz.innerTypeInstance (JS.CIPChirality.CIPAtom, this, null).create (b, null, false, true);
b2.canBePseudo = b2.isOddCumulene = isAxial;
var btop = this.getAtomChiralityLimited (b, b2, a2, ruleMax) - 1;
var c = 0;
if (atop >= 0 && btop >= 0) {
if (isAxial) {
c = (this.isPos (b2.atoms[btop], b2, a1, a1.atoms[atop]) ? 34 : 33);
if ((a1.ties == null) != (b2.ties == null)) c |= 4;
} else {
c = (this.isCis (b2.atoms[btop], b2, a1, a1.atoms[atop]) ? 8 : 16);
}}if (c != 0 && (isAxial || !this.isAtropisomeric (a) && !this.isAtropisomeric (b))) {
a.setCIPChirality (c);
b.setCIPChirality (c);
if (JU.Logger.debugging) JU.Logger.info (a + "-" + b + " " + JV.JC.getCIPChiralityName (c));
}return c;
}, "JU.Node,JU.Node,JU.Node,JU.Node,~B,~N");
Clazz.defineMethod (c$, "isAtropisomeric", 
 function (a) {
return this.bsAtropisomeric != null && this.bsAtropisomeric.get (a.getIndex ());
}, "JU.Node");
Clazz.defineMethod (c$, "isCis", 
function (a, b, c, d) {
JU.Measure.getNormalThroughPoints (a.atom.getXYZ (), b.atom.getXYZ (), c.atom.getXYZ (), this.vNorm, this.vTemp);
var vNorm2 =  new JU.V3 ();
JU.Measure.getNormalThroughPoints (b.atom.getXYZ (), c.atom.getXYZ (), d.atom.getXYZ (), vNorm2, this.vTemp);
return (this.vNorm.dot (vNorm2) > 0);
}, "JS.CIPChirality.CIPAtom,JS.CIPChirality.CIPAtom,JS.CIPChirality.CIPAtom,JS.CIPChirality.CIPAtom");
Clazz.defineMethod (c$, "isPos", 
function (a, b, c, d) {
var angle = JU.Measure.computeTorsion (a.atom.getXYZ (), b.atom.getXYZ (), c.atom.getXYZ (), d.atom.getXYZ (), true);
return (angle > 0);
}, "JS.CIPChirality.CIPAtom,JS.CIPChirality.CIPAtom,JS.CIPChirality.CIPAtom,JS.CIPChirality.CIPAtom");
Clazz.defineMethod (c$, "sign", 
function (score) {
return (score < 0 ? -1 : score > 0 ? 1 : 0);
}, "~N");
c$.$CIPChirality$CIPAtom$ = function () {
Clazz.pu$h(self.c$);
c$ = Clazz.decorateAsClass (function () {
Clazz.prepareCallback (this, arguments);
this.atom = null;
this.id = 0;
this.parent = null;
this.rootSubstituent = null;
this.elemNo = 0;
this.massNo = 0;
this.sphere = 0;
this.bsPath = null;
this.myPath = "";
this.rootDistance = 0;
this.nAtoms = 0;
this.nPriorities = 0;
this.h1Count = 0;
this.knownAtomChirality = "~";
this.isSet = false;
this.isDuplicate = true;
this.isTerminal = false;
this.isAlkene = false;
this.alkeneParent = null;
this.alkeneChild = null;
this.isAlkeneAtom2 = false;
this.doCheckPseudo = false;
this.isPseudo = false;
this.achiral = false;
this.bondCount = 0;
this.atoms = null;
this.priorities = null;
this.prevPriorities = null;
this.rule4List = null;
this.lonePair = null;
this.atomIndex = 0;
this.auxEZ = -1;
this.auxParentReversed = null;
this.auxPseudo = null;
this.canBePseudo = true;
this.ties = null;
this.isOddCumulene = false;
this.nextSP2 = null;
this.nextChiralBranch = null;
this.rule4Count = null;
this.priority = 0;
this.htPathPoints = null;
this.isTrigonalPyramidal = false;
this.isRingDuplicate = false;
Clazz.instantialize (this, arguments);
}, JS.CIPChirality, "CIPAtom", null, [Comparable, Cloneable]);
Clazz.prepareFields (c$, function () {
this.atoms =  new Array (4);
this.priorities =  Clazz.newIntArray (4, 0);
this.prevPriorities =  Clazz.newIntArray (-1, [-1, -1, -1, -1]);
});
Clazz.makeConstructor (c$, 
function () {
});
Clazz.defineMethod (c$, "create", 
function (a, b, c, d) {
this.id = ++this.b$["JS.CIPChirality"].ptID;
this.parent = b;
if (a == null) return this;
this.isAlkene = d;
this.atom = a;
this.elemNo = a.getElementNumber ();
this.massNo = a.getNominalMass ();
this.atomIndex = a.getIndex ();
this.bondCount = a.getCovalentBondCount ();
this.isTrigonalPyramidal = (this.bondCount == 3 && !d && (this.elemNo > 10 || this.b$["JS.CIPChirality"].bsAzacyclic != null && this.b$["JS.CIPChirality"].bsAzacyclic.get (this.atomIndex)));
if (this.isTrigonalPyramidal) this.getLonePair ();
this.canBePseudo = (this.bondCount == 4 || this.isTrigonalPyramidal);
var e = a.getCIPChirality (false);
if (e.equals ("") || e.equals ("r") || e.equals ("s")) e = "~";
this.knownAtomChirality = e;
if (b != null) this.sphere = b.sphere + 1;
if (this.sphere == 1) {
this.rootSubstituent = this;
this.htPathPoints =  new java.util.Hashtable ();
} else if (b != null) {
this.rootSubstituent = b.rootSubstituent;
this.htPathPoints = this.rootSubstituent.htPathPoints;
}this.bsPath = (b == null ?  new JU.BS () : JU.BSUtil.copy (b.bsPath));
var f = c;
if (b == null) {
this.bsPath.set (this.atomIndex);
this.rootDistance = 0;
} else if (f && this.b$["JS.CIPChirality"].bsAromatic != null && this.b$["JS.CIPChirality"].bsAromatic.get (this.atomIndex)) {
this.rootDistance = b.rootDistance;
} else if (a === this.b$["JS.CIPChirality"].root.atom) {
this.rootDistance = 0;
c = true;
} else if (this.bsPath.get (this.atomIndex)) {
c = true;
this.rootDistance = this.rootSubstituent.htPathPoints.get (a.toString ()).intValue ();
} else {
this.bsPath.set (this.atomIndex);
this.rootDistance = b.rootDistance + 1;
this.rootSubstituent.htPathPoints.put (a.toString (),  new Integer (this.rootDistance));
}this.isDuplicate = c;
this.myPath = (b != null ? b.myPath + "-" : "") + this;
if (JU.Logger.debugging) JU.Logger.info ("new CIPAtom " + this.myPath);
this.isRingDuplicate = (c && !f);
return this;
}, "JU.Node,JS.CIPChirality.CIPAtom,~B,~B");
Clazz.defineMethod (c$, "getLonePair", 
 function () {
var a = this.b$["JS.CIPChirality"].getTrigonality (this.atom, this.b$["JS.CIPChirality"].vNorm);
if (Math.abs (a) > 0.2) {
this.lonePair =  new JU.P3 ();
this.b$["JS.CIPChirality"].vNorm.scale (a);
this.lonePair.add2 (this.atom.getXYZ (), this.b$["JS.CIPChirality"].vNorm);
}});
Clazz.defineMethod (c$, "updateRingList", 
 function () {
var a = JU.BSUtil.newAndSetBit (this.atomIndex);
var b = this;
var c = -1;
while ((b = b.parent) != null && c != this.atomIndex) {
a.set (c = b.atomIndex);
}
if (a.cardinality () < 8) {
for (var d = this.b$["JS.CIPChirality"].lstSmallRings.size (); --d >= 0; ) if (this.b$["JS.CIPChirality"].lstSmallRings.get (d).equals (a)) return;

this.b$["JS.CIPChirality"].lstSmallRings.addLast (a);
}});
Clazz.defineMethod (c$, "set", 
function () {
if (this.isSet) return true;
this.isSet = true;
if (this.isDuplicate) return true;
var a = this.atom.getBondCount ();
var b = this.atom.getEdges ();
if (JU.Logger.debuggingHigh) JU.Logger.info ("set " + this);
var c = 0;
for (var d = 0; d < a; d++) {
var e = b[d];
if (!e.isCovalent ()) continue;
var f = e.getOtherAtomNode (this.atom);
var g = (this.parent != null && this.parent.atom === f);
var h = e.getCovalentOrder ();
if (h == 2) {
if (this.elemNo > 10 || !this.b$["JS.CIPChirality"].isFirstRow (f)) h = 1;
 else {
this.isAlkene = true;
if (g) {
this.knownAtomChirality = e.getCIPChirality (false);
if (this.knownAtomChirality.equals ("")) this.knownAtomChirality = "~";
if (this.atom.getCovalentBondCount () == 2 && this.atom.getValence () == 4) {
this.parent.isAlkeneAtom2 = false;
} else {
this.isAlkeneAtom2 = true;
}this.parent.alkeneChild = null;
this.alkeneParent = (this.parent.alkeneParent == null ? this.parent : this.parent.alkeneParent);
this.alkeneParent.alkeneChild = this;
if (this.parent.alkeneParent == null) this.parent.nextSP2 = this;
}}}if (a == 1 && h == 1 && g) {
this.isTerminal = true;
return true;
}switch (h) {
case 3:
if (this.addAtom (c++, f, g, false) == null) {
this.isTerminal = true;
return false;
}case 2:
if (this.addAtom (c++, f, h != 2 || g, h == 2) == null) {
this.isTerminal = true;
return false;
}case 1:
if (!g && this.addAtom (c++, f, h != 1 && this.elemNo <= 10, false) == null) {
this.isTerminal = true;
return false;
}break;
default:
this.isTerminal = true;
return false;
}
}
this.isTerminal = (c == 0);
this.nAtoms = c;
for (; c < this.atoms.length; c++) this.atoms[c] = Clazz.innerTypeInstance (JS.CIPChirality.CIPAtom, this, null).create (null, this, true, false);

var e = this.b$["JS.CIPChirality"].currentRule;
this.b$["JS.CIPChirality"].currentRule = 1;
java.util.Arrays.sort (this.atoms);
this.b$["JS.CIPChirality"].currentRule = e;
if (this.isTerminal) System.out.println ("????");
return !this.isTerminal;
});
Clazz.defineMethod (c$, "addAtom", 
function (a, b, c, d) {
if (a >= this.atoms.length) {
if (JU.Logger.debugging) JU.Logger.info (" too many bonds on " + this.atom);
return null;
}if (this.parent == null) {
var e = b.getAtomicAndIsotopeNumber ();
if (e == 1) {
if (++this.h1Count > 1) {
if (JU.Logger.debuggingHigh) JU.Logger.info (" second H atom found on " + this.atom);
return null;
}}}this.atoms[a] = Clazz.innerTypeInstance (JS.CIPChirality.CIPAtom, this, null).create (b, this, c, d);
if (this.b$["JS.CIPChirality"].currentRule > 3) {
this.prevPriorities[a] = this.atoms[a].getBasePriority (true);
}return this.atoms[a];
}, "~N,JU.Node,~B,~B");
Clazz.defineMethod (c$, "sortSubstituents", 
function () {
var a =  Clazz.newIntArray (4, 0);
this.ties = null;
for (var b = 0; b < 4; b++) {
this.priorities[b] = 0;
if (this.prevPriorities[b] == -1 && this.b$["JS.CIPChirality"].currentRule > 3) {
this.prevPriorities[b] = this.atoms[b].getBasePriority (true);
}}
if (JU.Logger.debugging) {
JU.Logger.info (this.b$["JS.CIPChirality"].root + "---sortSubstituents---" + this);
for (var c = 0; c < 4; c++) {
JU.Logger.info (this.b$["JS.CIPChirality"].getRuleName () + ": " + this + "[" + c + "]=" + this.atoms[c].myPath + " " + Integer.toHexString (this.prevPriorities[c]));
}
JU.Logger.info ("---");
}var c = (this.b$["JS.CIPChirality"].currentRule > 4 && this.rule4List != null);
for (var d = 0; d < 4; d++) {
var e = this.atoms[d];
for (var f = d + 1; f < 4; f++) {
var g = this.atoms[f];
var h = JU.Logger.debuggingHigh && g.isHeavy () && e.isHeavy ();
var i = (e.atom == null ? 1 : g.atom == null ? -1 : this.prevPriorities[d] == this.prevPriorities[f] ? 0 : this.prevPriorities[f] < this.prevPriorities[d] ? 1 : -1);
if (i == 0) i = (c ? this.checkRule4And5 (d, f) : e.compareTo (g));
if (h) JU.Logger.info (this.dots () + "ordering " + this.id + "." + d + "." + f + " " + this + "-" + e + " vs " + g + " = " + i);
switch (i) {
case -2147483648:
if (c && this.sphere == 0) this.achiral = true;
a[d]++;
if (h) JU.Logger.info (this.dots () + this.atom + "." + g + " ends up with tie with " + e);
break;
case 1:
a[d]++;
this.priorities[d]++;
if (h) JU.Logger.info (this.dots () + this + "." + g + " B-beats " + e);
break;
case -1:
a[f]++;
this.priorities[f]++;
if (h) JU.Logger.info (this.dots () + this + "." + e + " A-beats " + g);
break;
case 0:
i = e.breakTie (g);
switch (this.b$["JS.CIPChirality"].sign (i)) {
case 0:
a[d]++;
if (h) JU.Logger.info (this.dots () + this + "." + g + " ends up with tie with " + e);
break;
case 1:
a[d]++;
this.priorities[d]++;
if (h) JU.Logger.info (this.dots () + this + "." + g + " wins in tie with " + e);
break;
case -1:
a[f]++;
this.priorities[f]++;
if (h) JU.Logger.info (this.dots () + this + "." + e + " wins in tie with " + g);
break;
}
break;
}
if (this.doCheckPseudo) {
this.doCheckPseudo = false;
if (this.ties == null) this.ties =  new JU.Lst ();
this.ties.addLast ( Clazz.newIntArray (-1, [d, f]));
}}
}
var e =  new Array (4);
var f =  Clazz.newIntArray (4, 0);
var g =  Clazz.newIntArray (4, 0);
var h =  new JU.BS ();
var i = JS.CIPChirality.PRIORITY_SHIFT[this.b$["JS.CIPChirality"].currentRule];
for (var j = 0; j < 4; j++) {
var k = a[j];
var l = e[k] = this.atoms[j];
var m = this.priorities[j];
f[k] = m;
var n = this.prevPriorities[j];
if (n < 0) n = 0;
n |= (m << i);
g[k] = n;
if (l.atom != null) h.set (this.priorities[j]);
}
this.atoms = e;
this.priorities = f;
this.prevPriorities = g;
this.nPriorities = h.cardinality ();
if (this.nPriorities > this.b$["JS.CIPChirality"].nPriorityMax) this.b$["JS.CIPChirality"].nPriorityMax = this.nPriorities;
if (this.ties != null && !this.isOddCumulene) {
switch (this.ties.size ()) {
case 1:
switch (this.checkPseudoHandedness (this.ties.get (0), a)) {
case 1:
case 2:
this.isPseudo = this.canBePseudo;
break;
}
break;
case 2:
this.canBePseudo = false;
break;
}
}if (JU.Logger.debugging) {
JU.Logger.info (this.dots () + this.atom + " nPriorities = " + this.nPriorities);
for (var k = 0; k < 4; k++) {
JU.Logger.info (this.dots () + this.myPath + "[" + k + "]=" + this.atoms[k] + " " + this.priorities[k] + " " + Integer.toHexString (this.prevPriorities[k]) + " new");
}
JU.Logger.info (this.dots () + "-------");
}});
Clazz.defineMethod (c$, "dots", 
 function () {
return ".....................".substring (0, Math.min (20, this.sphere));
});
Clazz.defineMethod (c$, "breakTie", 
 function (a) {
if (JU.Logger.debugging && this.isHeavy () && a.isHeavy ()) JU.Logger.info (this.dots () + "tie for " + this + " and " + a + " at sphere " + this.sphere);
if (this.isDuplicate && a.isDuplicate && this.atom === a.atom && this.rootDistance == a.rootDistance) return 0;
var b = this.checkNoSubs (a);
if (b != 0) return b * (this.sphere + 1);
if (!this.set () || !a.set () || this.isTerminal && a.isTerminal || this.isDuplicate && a.isDuplicate) return 0;
if (this.isTerminal != a.isTerminal) return (this.isTerminal ? 1 : -1) * (this.sphere + 1);
if (this.b$["JS.CIPChirality"].currentRule == 2) {
this.preSortRule1b ();
a.preSortRule1b ();
}if ((b = this.compareShallowly (a)) != 0) return b;
this.sortSubstituents ();
a.sortSubstituents ();
return this.compareDeeply (a);
}, "JS.CIPChirality.CIPAtom");
Clazz.defineMethod (c$, "preSortRule1b", 
 function () {
var a;
var b;
for (var c = 0; c < 3; c++) {
if (!(a = this.atoms[c]).isDuplicate) continue;
for (var d = c + 1; d < 4; d++) {
if (!(b = this.atoms[d]).isDuplicate || a.elemNo != b.elemNo || a.rootDistance <= b.rootDistance) continue;
this.atoms[c] = b;
this.atoms[d] = a;
}
}
});
Clazz.defineMethod (c$, "isHeavy", 
 function () {
return this.massNo > 1;
});
Clazz.defineMethod (c$, "compareShallowly", 
 function (a) {
for (var b = 0; b < this.nAtoms; b++) {
var c = this.atoms[b];
var d = a.atoms[b];
var e = c.checkCurrentRule (d);
if (e == -2147483648) e = 0;
if (e != 0) {
if (JU.Logger.debugging && c.isHeavy () && d.isHeavy ()) JU.Logger.info (c.dots () + "compareShallow " + c + " " + d + ": " + e * c.sphere);
return e * c.sphere;
}}
return 0;
}, "JS.CIPChirality.CIPAtom");
Clazz.defineMethod (c$, "compareDeeply", 
 function (a) {
var b = (this.nAtoms == 0 ? 1 : 0);
var c = 2147483647;
for (var d = 0; d < this.nAtoms; d++) {
var e = this.atoms[d];
var f = a.atoms[d];
if (JU.Logger.debugging && e.isHeavy () && f.isHeavy ()) JU.Logger.info (e.dots () + "compareDeep sub " + e + " " + f);
var g = e.breakTie (f);
if (g == 0) continue;
var h = Math.abs (g);
if (JU.Logger.debugging && e.isHeavy () && f.isHeavy ()) JU.Logger.info (e.dots () + "compareDeep sub " + e + " " + f + ": " + g);
if (h < c) {
c = h;
b = g;
}}
if (JU.Logger.debugging) JU.Logger.info (this.dots () + "compareDeep " + this + " " + a + ": " + b);
return b;
}, "JS.CIPChirality.CIPAtom");
Clazz.overrideMethod (c$, "compareTo", 
function (a) {
var b;
return (a == null ? -1 : (this.atom == null) != (a.atom == null) ? (this.atom == null ? 1 : -1) : (b = this.checkCurrentRule (a)) == -2147483648 ? 0 : b != 0 ? b : this.checkNoSubs (a));
}, "JS.CIPChirality.CIPAtom");
Clazz.defineMethod (c$, "checkNoSubs", 
 function (a) {
return a.isDuplicate == this.isDuplicate ? 0 : a.isDuplicate ? -1 : 1;
}, "JS.CIPChirality.CIPAtom");
Clazz.defineMethod (c$, "checkCurrentRule", 
function (a) {
switch (this.b$["JS.CIPChirality"].currentRule) {
default:
case 1:
return this.checkRule1a (a);
case 2:
return this.checkRule1b (a);
case 3:
return this.checkRule2 (a);
case 4:
return this.checkRule3 (a);
case 5:
return 0;
case 6:
return this.checkRule5 (a);
}
}, "JS.CIPChirality.CIPAtom");
Clazz.defineMethod (c$, "checkRule1a", 
 function (a) {
return a.atom === this.atom ? 0 : a.atom == null ? -1 : this.atom == null ? 1 : a.elemNo < this.elemNo ? -1 : a.elemNo > this.elemNo ? 1 : 0;
}, "JS.CIPChirality.CIPAtom");
Clazz.defineMethod (c$, "checkRule1b", 
 function (a) {
return !a.isDuplicate || !this.isDuplicate ? 0 : a.rootDistance == this.rootDistance ? 0 : a.rootDistance > this.rootDistance ? -1 : 1;
}, "JS.CIPChirality.CIPAtom");
Clazz.defineMethod (c$, "checkRule2", 
 function (a) {
return a.massNo < this.massNo ? -1 : a.massNo > this.massNo ? 1 : 0;
}, "JS.CIPChirality.CIPAtom");
Clazz.defineMethod (c$, "checkRule3", 
 function (a) {
var b;
var c;
return this.parent == null || !this.parent.isAlkeneAtom2 || !a.parent.isAlkeneAtom2 || this.isDuplicate || a.isDuplicate || !this.isCumulativeType (-2) || !a.isCumulativeType (-2) ? -2147483648 : this.parent === a.parent ? this.b$["JS.CIPChirality"].sign (this.breakTie (a)) : (b = this.parent.getEZaux ()) < (c = a.parent.getEZaux ()) ? -1 : b > c ? 1 : 0;
}, "JS.CIPChirality.CIPAtom");
Clazz.defineMethod (c$, "isCumulativeType", 
 function (a) {
return (this.parent != null && this.parent.isAlkeneAtom2 && ((this.parent.alkeneParent.sphere + this.parent.sphere) % 2) == (a == -2 ? 1 : 2));
}, "~N");
Clazz.defineMethod (c$, "getEZaux", 
 function () {
if (this.auxEZ == -1 && (this.auxEZ = this.alkeneParent.auxEZ) == -1) {
var a = null;
var b = null;
var c = null;
this.auxEZ = 24;
this.sortSubstituents ();
b = this.getTopAtom ();
if (b != null) {
if (this.auxParentReversed == null) {
if (JU.Logger.debugging) JU.Logger.info ("reversing path for " + this.alkeneParent);
c = this.alkeneParent.clone ();
c.addReturnPath (this.alkeneParent.nextSP2, this.alkeneParent);
} else {
c = this.auxParentReversed;
}c.sortSubstituents ();
a = c.getTopAtom ();
if (a != null) {
this.auxEZ = (this.b$["JS.CIPChirality"].isCis (b, this, c, a) ? 8 : 16);
}}}this.alkeneParent.auxEZ = this.auxEZ;
if (JU.Logger.debugging) JU.Logger.info ("getZaux " + this.alkeneParent + " " + this.auxEZ);
return this.auxEZ;
});
Clazz.defineMethod (c$, "getReturnPath", 
 function (a) {
var b =  new JU.Lst ();
while (a.parent != null && a.parent.atoms[0] != null) {
if (JU.Logger.debugging) JU.Logger.info ("path:" + a.parent.atom + "->" + a.atom);
b.addLast (a = a.parent);
}
b.addLast (null);
return b;
}, "JS.CIPChirality.CIPAtom");
Clazz.defineMethod (c$, "addReturnPath", 
 function (a, b) {
var c = this.getReturnPath (b);
var d = this;
for (var e = 0, f = c.size (); e < f; e++) {
var g = c.get (e);
if (g == null) {
g = Clazz.innerTypeInstance (JS.CIPChirality.CIPAtom, this, null).create (null, this, true, this.isAlkene);
} else {
var h = g.sphere;
g = g.clone ();
g.sphere = h + 1;
}d.replaceParentSubstituent (a, g);
if (a == null) break;
a = a.parent;
d = g;
}
}, "JS.CIPChirality.CIPAtom,JS.CIPChirality.CIPAtom");
Clazz.defineMethod (c$, "getBasePriority", 
function (a) {
return (this.atom == null ? 2147479552 : ((127 - this.elemNo) << JS.CIPChirality.PRIORITY_SHIFT[1]) | (a ? (255 - this.massNo) << JS.CIPChirality.PRIORITY_SHIFT[3] : 0));
}, "~B");
Clazz.defineMethod (c$, "checkRule4And5", 
 function (a, b) {
if (this.rule4List[a] == null && this.rule4List[b] == null) return 0;
if (this.rule4List[a] == null || this.rule4List[b] == null) return this.rule4List[b] == null ? -1 : 1;
return this.compareRootMataPair (a, b);
}, "~N,~N");
Clazz.defineMethod (c$, "compareRootMataPair", 
 function (a, b) {
var c = (this.b$["JS.CIPChirality"].currentRule == 6);
var d = this.rule4List[a].substring (1);
var e = this.rule4List[b].substring (1);
if (this.atoms[a].nextChiralBranch != null) {
var f = this.atoms[a].getMataList (this.getFirstRef (d), c);
d = (f.indexOf ("|") < 0 ? d + f : f);
}if (this.atoms[b].nextChiralBranch != null) {
var f = this.atoms[b].getMataList (this.getFirstRef (e), c);
e = (f.indexOf ("|") < 0 ? e + f : f);
}if (JU.Logger.debugging) JU.Logger.info (this.dots () + this + " comparing " + this.atoms[a] + " " + d + " to " + this.atoms[b] + " " + e);
if (d.length != e.length) return 0;
if (c) return d.compareTo (e);
if (d.indexOf ("|") >= 0 || e.indexOf ("|") >= 0) {
var f = JU.PT.split (d, "|");
var g = JU.PT.split (e, "|");
var h = 2147483647;
var i = 0;
d = f[0];
e = g[0];
for (var j = 0; j < 2; j++) {
for (var k = 0; k < 2; k++) {
var l = this.compareRule4PairStr (f[j], g[k], true);
i += l;
if (l != 0 && Math.abs (l) <= h) {
h = Math.abs (l);
d = f[j];
e = g[k];
}}
}
if (i == 0) return 0;
}d = JU.PT.rep (d, "~", "");
e = JU.PT.rep (e, "~", "");
if (d.length == 1 && "RS".indexOf (d) < 0) {
var f = this.checkEnantiomer (d, e, 0, d.length, " rs");
switch (f) {
case -1:
case 1:
this.canBePseudo = false;
this.doCheckPseudo = true;
return f;
}
}return this.compareRule4PairStr (d, e, false);
}, "~N,~N");
Clazz.defineMethod (c$, "getFirstRef", 
 function (a) {
for (var b = 0, c = a.length; b < c; b++) {
var d = this.fixMataRef (a.charAt (b));
switch (d) {
case 'R':
case 'S':
return "" + d;
}
}
return null;
}, "~S");
Clazz.defineMethod (c$, "getMataList", 
 function (a, b) {
var c = 0;
for (var d = this.rule4List.length; --d >= 0; ) if (this.rule4List[d] != null) c++;

var e =  new Array (c);
for (var f = c, g = this.rule4List.length; --g >= 0; ) if (this.rule4List[g] != null) {
e[--f] = this.rule4List[g];
}
if (a == null) {
a = this.getMataRef (b);
} else {
for (var h = 0; h < c; h++) e[h] = "." + e[h].substring (1);

}switch (a.length) {
default:
case 1:
return this.getMataSequence (e, a, b);
case 2:
return this.getMataSequence (e, "R", false) + "|" + this.getMataSequence (e, "S", false);
}
}, "~S,~B");
Clazz.defineMethod (c$, "getMataRef", 
 function (a) {
var b = a ? "R" : this.rule4Count[1] > this.rule4Count[2] ? "R" : this.rule4Count[1] < this.rule4Count[2] ? "S" : "RS";
if (JU.Logger.debugging) JU.Logger.info (this + "mata ref: " + b + " Rule5?" + a + " " + JU.PT.toJSON ("rule4Count", this.rule4Count));
return b;
}, "~B");
Clazz.defineMethod (c$, "getMataSequence", 
 function (a, b, c) {
var d = a.length;
var e =  new Array (d);
for (var f = d, g = this.rule4List.length; --g >= 0; ) {
if (this.rule4List[g] != null) {
--f;
e[f] = a[f];
if (this.atoms[g].nextChiralBranch != null) e[f] += this.atoms[g].nextChiralBranch.getMataList (b, c);
}}
var h = (c ? e : this.getMataSortedList (e, b));
var i = 0;
for (var j = 0; j < d; j++) {
var k = h[j];
if (k.length > i) i = k.length;
}
var k = "";
var l;
for (var m = 1; m < i; m++) {
for (var n = 0; n < d; n++) {
var o = h[n];
if (m < o.length && (l = o.charAt (m)) != '~' && l != ';') k += l;
}
if (c) {
for (var o = 0; o < d; o++) {
var p = h[o];
if (m < p.length) h[o] = p.substring (0, m) + "~" + p.substring (m + 1);
}
java.util.Arrays.sort (h);
}}
return k;
}, "~A,~S,~B");
Clazz.defineMethod (c$, "compareRule4PairStr", 
 function (a, b, c) {
if (JU.Logger.debugging) JU.Logger.info (this.dots () + this + " Rule 4b comparing " + a + " " + b);
this.doCheckPseudo = false;
var d = a.length;
if (d == 0 || d != b.length) return 0;
var e = this.fixMataRef (a.charAt (0));
var f = this.fixMataRef (b.charAt (0));
for (var g = 1; g < d; g++) {
var h = (e == this.fixMataRef (a.charAt (g)));
var i = (f == this.fixMataRef (b.charAt (g)));
if (h != i) return (c ? g : 1) * (h ? -1 : 1);
}
if (c) return 0;
if (e == f) return -2147483648;
if (!this.canBePseudo) this.b$["JS.CIPChirality"].root.canBePseudo = false;
this.doCheckPseudo = this.canBePseudo && (e == 'R' || e == 'S');
return e < f ? -1 : 1;
}, "~S,~S,~B");
Clazz.defineMethod (c$, "fixMataRef", 
 function (a) {
switch (a) {
case 'R':
case 'M':
case 'Z':
return 'R';
case 'S':
case 'P':
case 'E':
return 'S';
default:
return a;
}
}, "~S");
Clazz.defineMethod (c$, "getMataSortedList", 
 function (a, b) {
var c = a.length;
var d =  new Array (c);
for (var e = 0; e < c; e++) d[e] = JU.PT.rep (a[e], b, "A");

java.util.Arrays.sort (d);
for (var f = 0; f < c; f++) d[f] = JU.PT.rep (d[f], "A", b);

if (JU.Logger.debuggingHigh) for (var g = 0; g < c; g++) JU.Logger.info ("Sorted Mata list " + g + " " + b + ": " + d[g]);

return d;
}, "~A,~S");
Clazz.defineMethod (c$, "createAuxiliaryRSCenters", 
function (a, b) {
if (this.auxParentReversed != null) this.auxParentReversed.createAuxiliaryRSCenters (null, null);
if (this.auxPseudo != null) this.auxPseudo.createAuxiliaryRSCenters (null, null);
var c = -1;
var d = "";
var e = (a == null ? "" : "~");
var f = false;
if (this.atom != null) {
this.rule4List =  new Array (4);
var g =  Clazz.newIntArray (4, 0);
var h = 0;
var i =  new Array (1);
for (var j = 0; j < 4; j++) {
var k = this.atoms[j];
if (k != null) k.set ();
if (k != null && !k.isDuplicate && !k.isTerminal) {
k.priority = this.priorities[j];
i[0] = null;
var l = k.createAuxiliaryRSCenters (a == null ? k : a, i);
if (i[0] != null) {
k.nextChiralBranch = i[0];
if (b != null) b[0] = i[0];
}this.rule4List[j] = k.priority + l;
if (k.nextChiralBranch != null || this.isChiralSequence (l)) {
g[h] = j;
h++;
d += l;
} else {
this.rule4List[j] = null;
}}}
var k = 0;
switch (h) {
case 0:
d = "";
break;
case 1:
break;
case 2:
if (a != null) {
switch (k = (this.compareRule4aEnantiomers (this.rule4List[g[0]], this.rule4List[g[1]]))) {
case 2147483647:
f = true;
e = "";
break;
case -2147483648:
e = "";
f = true;
k = 0;
break;
case 0:
f = true;
e = "u";
d = "";
if (b != null) b[0] = null;
break;
case -1:
case 1:
f = true;
d = "";
break;
}
}break;
case 3:
case 4:
e = "";
f = true;
}
if (f) {
d = "";
if (b != null && e !== "u") b[0] = this;
}if (!f || k == -1 || k == 1) {
if (this.isAlkene && this.alkeneChild != null) {
} else if (a != null && (this.bondCount == 4 && this.nPriorities >= 3 - Math.abs (k) || this.isTrigonalPyramidal && this.nPriorities >= 2 - Math.abs (k))) {
if (f) {
switch (this.checkPseudoHandedness (g, null)) {
case 1:
e = "r";
break;
case 2:
e = "s";
break;
}
d = "";
if (b != null) b[0] = null;
} else {
var l = this.clone ();
if (l.set ()) {
l.addReturnPath (null, this);
var m = this.b$["JS.CIPChirality"].currentRule;
this.b$["JS.CIPChirality"].currentRule = 1;
l.sortSubstituents ();
this.b$["JS.CIPChirality"].currentRule = m;
c = l.checkHandedness ();
e = (c == 1 ? "R" : c == 2 ? "S" : "~");
a.addMataRef (this.sphere, this.priority, c);
}}}}}e += d;
if (JU.Logger.debugging && !e.equals ("~")) JU.Logger.info ("creating aux " + this.myPath + e);
return e;
}, "JS.CIPChirality.CIPAtom,~A");
Clazz.defineMethod (c$, "isChiralSequence", 
 function (a) {
return a.indexOf ("R") >= 0 || a.indexOf ("S") >= 0 || a.indexOf ("r") >= 0 || a.indexOf ("s") >= 0 || a.indexOf ("u") >= 0;
}, "~S");
Clazz.defineMethod (c$, "addMataRef", 
 function (a, b, c) {
if (this.rule4Count == null) {
this.rule4Count =  Clazz.newIntArray (-1, [2147483647, 0, 0]);
}var d = a * 10 + b;
if (d <= this.rule4Count[0]) {
if (d < this.rule4Count[0]) {
this.rule4Count[0] = d;
this.rule4Count[1] = this.rule4Count[2] = 0;
}this.rule4Count[c]++;
}}, "~N,~N,~N");
Clazz.defineMethod (c$, "compareRule4aEnantiomers", 
 function (a, b) {
if (a.indexOf ("R") < 0 && a.indexOf ("S") < 0 || a.charAt (0) != b.charAt (0)) return -2147483648;
var c = a.length;
if (c != b.length) return -2147483648;
if (a.equals (b)) return 0;
System.out.println ("testing ~RS here with " + a + " and " + b);
return this.checkEnantiomer (a, b, 1, c, "~RS");
}, "~S,~S");
Clazz.defineMethod (c$, "checkEnantiomer", 
 function (a, b, c, d, e) {
var f = 0;
for (var g = c; g < d; g++) {
var h = e.indexOf (a.charAt (g));
var i = h + e.indexOf (b.charAt (g));
if (i != 0 && i != 3) return 2147483647;
if (f == 0) f = (h == 1 ? -1 : 1);
}
return f;
}, "~S,~S,~N,~N,~S");
Clazz.defineMethod (c$, "checkPseudoHandedness", 
 function (a, b) {
var c = (b == null ? a[0] : b[a[0]]);
var d = (b == null ? a[1] : b[a[1]]);
var e;
if (this.auxPseudo == null) {
e = this.clone ();
e.atoms[c] = Clazz.innerTypeInstance (JS.CIPChirality.CIPAtom, this, null).create (null, e, false, this.isAlkene);
e.atoms[d] = Clazz.innerTypeInstance (JS.CIPChirality.CIPAtom, this, null).create (null, e, false, this.isAlkene);
e.addReturnPath (null, this);
} else {
e = this.auxPseudo;
}var f = this.b$["JS.CIPChirality"].currentRule;
this.b$["JS.CIPChirality"].currentRule = 1;
e.sortSubstituents ();
this.b$["JS.CIPChirality"].currentRule = f;
e.atoms[this.bondCount - 2] = this.atoms[Math.min (c, d)];
e.atoms[this.bondCount - 1] = this.atoms[Math.max (c, d)];
var g = e.checkHandedness ();
if (JU.Logger.debugging) {
for (var h = 0; h < 4; h++) JU.Logger.info ("pseudo " + g + " " + this.priorities[h] + " " + this.atoms[h].myPath);

}return g;
}, "~A,~A");
Clazz.defineMethod (c$, "replaceParentSubstituent", 
 function (a, b) {
for (var c = 0; c < 4; c++) if (this.atoms[c] === a || a == null && this.atoms[c].atom == null) {
this.atoms[c] = b;
if (JU.Logger.debugging) JU.Logger.info ("replace " + this + "[" + c + "]=" + b);
this.prevPriorities[c] = this.atoms[c].getBasePriority (true);
this.parent = a;
return;
}
}, "JS.CIPChirality.CIPAtom,JS.CIPChirality.CIPAtom");
Clazz.defineMethod (c$, "getTopAtom", 
 function () {
var a = (this.atoms[0].isDuplicate ? 1 : 0);
return this.priorities[a] == this.priorities[a + 1] ? null : this.priorities[a] < this.priorities[a + 1] ? this.atoms[a] : this.atoms[a + 1];
});
Clazz.defineMethod (c$, "checkRule5", 
 function (a) {
if (this.isTerminal || this.isDuplicate) return 0;
var b = ";SRPMTC;".indexOf (this.knownAtomChirality);
var c = ";SRPMTC;".indexOf (a.knownAtomChirality);
return (b == c ? 0 : b > c ? -1 : 1);
}, "JS.CIPChirality.CIPAtom");
Clazz.defineMethod (c$, "checkHandedness", 
function () {
var a = this.atoms[0].atom.getXYZ ();
var b = this.atoms[1].atom.getXYZ ();
var c = this.atoms[2].atom.getXYZ ();
var d = (this.lonePair == null ? this.atoms[3].atom.getXYZ () : this.lonePair);
var e = JU.Measure.getNormalThroughPoints (a, b, c, this.b$["JS.CIPChirality"].vNorm, this.b$["JS.CIPChirality"].vTemp);
return (JU.Measure.distanceToPlaneV (this.b$["JS.CIPChirality"].vNorm, e, d) > 0 ? 1 : 2);
});
Clazz.defineMethod (c$, "clone", 
function () {
var a = null;
try {
a = Clazz.superCall (this, JS.CIPChirality.CIPAtom, "clone", []);
} catch (e) {
if (Clazz.exceptionOf (e, CloneNotSupportedException)) {
} else {
throw e;
}
}
a.id = this.b$["JS.CIPChirality"].ptID++;
a.atoms =  new Array (4);
a.priorities =  Clazz.newIntArray (4, 0);
a.prevPriorities =  Clazz.newIntArray (-1, [-1, -1, -1, -1]);
a.htPathPoints = this.htPathPoints;
for (var b = 0; b < 4; b++) {
a.priorities[b] = this.priorities[b];
if (this.atoms[b] != null) {
a.atoms[b] = this.atoms[b];
a.prevPriorities[b] = this.atoms[b].getBasePriority (true);
}}
if (JU.Logger.debugging) JU.Logger.info ("cloning " + this + " as " + a);
return a;
});
Clazz.defineMethod (c$, "toString", 
function () {
return (this.atom == null ? "<null>" : "[" + this.b$["JS.CIPChirality"].currentRule + "." + this.sphere + "," + this.rootDistance + "." + this.id + "." + this.atom.getAtomName () + (this.isDuplicate ? "*" : "") + "]");
});
c$ = Clazz.p0p ();
};
Clazz.defineStatics (c$,
"NO_CHIRALITY", 0,
"TIED", 0,
"B_WINS", 1,
"A_WINS", -1,
"DIASTEREOMERIC", 2147483647,
"IGNORE", -2147483648,
"NOT_RELEVANT", -2147483648,
"STEREO_SAME", 2147483647,
"STEREO_UNDETERMINED", -1,
"STEREO_RS", -1,
"STEREO_EZ", -2,
"STEREO_ALLENE", -3,
"STEREO_R", 1,
"STEREO_S", 2,
"STEREO_M", 33,
"STEREO_P", 34,
"STEREO_Z", 8,
"STEREO_E", 16,
"STEREO_BOTH_RS", 3,
"STEREO_BOTH_EZ", 24,
"RULE_1a", 1,
"RULE_1b", 2,
"RULE_2", 3,
"RULE_3", 4,
"RULE_4", 5,
"RULE_5", 6,
"PRIORITY_12_MASK", 0x7FFFF000,
"PRIORITY_1b_MASK", 0x00F00000,
"PRIORITY_SHIFT",  Clazz.newIntArray (-1, [-1, 24, 20, 12, 9, 6, 3, 0]),
"TRIGONALITY_MIN", 0.2);
});
