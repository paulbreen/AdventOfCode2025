// main.go
package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"time"
)

type Point struct {
	x, y, z int
}

type Pair struct {
	i, j   int
	distSq float64
}

// Union-Find
type DSU struct {
	parent []int
	size   []int
	count  int
}

func NewDSU(n int) *DSU {
	p := make([]int, n)
	s := make([]int, n)
	for i := 0; i < n; i++ {
		p[i] = i
		s[i] = 1
	}
	return &DSU{parent: p, size: s, count: n}
}

func (d *DSU) find(x int) int {
	if d.parent[x] != x {
		d.parent[x] = d.find(d.parent[x])
	}
	return d.parent[x]
}

func (d *DSU) unite(a, b int) bool {
	ra := d.find(a)
	rb := d.find(b)
	if ra == rb {
		return false
	}
	if d.size[ra] < d.size[rb] {
		ra, rb = rb, ra
	}
	d.parent[rb] = ra
	d.size[ra] += d.size[rb]
	d.count--
	return true
}

func loadPoints(path string) ([]Point, error) {
	f, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer f.Close()
	sc := bufio.NewScanner(f)
	var pts []Point
	for sc.Scan() {
		var x, y, z int
		_, err := fmt.Sscanf(sc.Text(), "%d,%d,%d", &x, &y, &z)
		if err != nil {
			return nil, err
		}
		pts = append(pts, Point{x, y, z})
	}
	return pts, nil
}

func main() {
	pts, err := loadPoints("input.txt")
	if err != nil {
		fmt.Println("Error: missing or invalid input.txt")
		return
	}
	n := len(pts)

	// Generate all pairs
	pairs := make([]Pair, 0, n*(n-1)/2)
	for i := 0; i < n; i++ {
		for j := i + 1; j < n; j++ {
			dx := float64(pts[i].x - pts[j].x)
			dy := float64(pts[i].y - pts[j].y)
			dz := float64(pts[i].z - pts[j].z)
			pairs = append(pairs, Pair{
				i:      i,
				j:      j,
				distSq: dx*dx + dy*dy + dz*dz,
			})
		}
	}

	// Sort by distance
	sort.Slice(pairs, func(a, b int) bool { return pairs[a].distSq < pairs[b].distSq })

	// Puzzle 1
	start1 := time.Now()
	dsu1 := NewDSU(n)
	connections := 0
	for _, p := range pairs {
		if dsu1.unite(p.i, p.j) {
			connections++
			if connections == 1000 {
				break
			}
		}
	}
	// compute largest 3 components
	compSize := make(map[int]int)
	for i := 0; i < n; i++ {
		r := dsu1.find(i)
		compSize[r]++
	}
	sizes := make([]int, 0, len(compSize))
	for _, v := range compSize {
		sizes = append(sizes, v)
	}
	sort.Sort(sort.Reverse(sort.IntSlice(sizes)))
	res1 := sizes[0] * sizes[1] * sizes[2]
	dur1 := time.Since(start1)

	// Puzzle 2
	start2 := time.Now()
	dsu2 := NewDSU(n)
	var lastPair Pair
	for _, p := range pairs {
		if dsu2.unite(p.i, p.j) {
			if dsu2.count == 1 {
				lastPair = p
				break
			}
		}
	}
	// product of X coordinates
	res2 := pts[lastPair.i].x * pts[lastPair.j].x
	dur2 := time.Since(start2)

	fmt.Printf("Puzzle 1: %d\n", res1)
	fmt.Printf("Puzzle 2: %d\n", res2)
	fmt.Printf("Total Duration: %dms\n", (dur1+dur2).Milliseconds())
}
