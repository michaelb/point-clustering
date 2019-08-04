Project Algo
===========

Authors: Michael Bleuez and Clement Malleret
--------------------------------------------

**Goal**:
The project aims to find the size of "clusters" within a set of points.
(A cluster is a connex composant)

**Performance**:
* A perfomance table (versions of the program, input format and execution time) is available in math/perfs.ods
* Complexity is roughly of __O(n.log(n).a^k)__ with n the number of points, a~2.2 a constant and k dimension of input space,
	however actual execution time vary a lot depending on properties of input;
	1. how much there are points interlinked (big clusters are detrimental in general) (or how big is distance relative to number of points)
	2. randomness of the distribution: uniformly distributed allow faster resolution, **to a big extent**
* Real-world speed: at this point of the project, our algorithm can process any reasonable (random-like, 2D) input of size 20k in ~0.5s (i5 4210U 1.7Ghz, SATA SSD)
	It is really hard to create a non-random distribution that is really the *worst* possible, but we have been able to slow the algorithm up to 60 sec (still 20k points.)
	For reference a 100% naïve algorithm take up to 8 minutes to solve (any) 20k-sized input.


**Etymology**:
* cluster: are "connex composant", is a class of objects. Cluster object include reference to the points they contain, which themselves know which cluster they are a part of
* quadrillage: divide the space in "cases" 
* points: are given a reference to an unique to a cluster object (containing only said point at first) at their creation. merge is done via merge method of cluster object
* density: relative to the given *distance*, how much the space is 'crowded'. A good exemple is that same-density sets have clusters of same ratio (size of cluster)/(total number of points) 
* a-types: are input where the points are quite sparse (relative to the given distance); an a-type input will contain only few tuples and a pletoria of singletons
* b-types: are inputs contains too much points relative to the given distance, thus is usually one extra large cluster and a few others


