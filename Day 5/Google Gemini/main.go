package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
	"time"
)

type Range struct {
	Start int
	End   int
}

func (r Range) isFresh(id int) bool {
	return id >= r.Start && id <= r.End
}

func parseInput(filename string) ([]Range, []int, error) {
	file, err := os.Open(filename)
	if err != nil {
		return nil, nil, fmt.Errorf("could not open file: %w", err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	ranges := []Range{}
	ids := []int{}
	parsingRanges := true

	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if line == "" {
			parsingRanges = false
			continue
		}

		if parsingRanges {
			parts := strings.Split(line, "-")
			if len(parts) != 2 {
				return nil, nil, fmt.Errorf("invalid range format: %s", line)
			}
			start, err1 := strconv.Atoi(parts[0])
			end, err2 := strconv.Atoi(parts[1])

			if err1 != nil || err2 != nil {
				return nil, nil, fmt.Errorf("invalid number in range: %s", line)
			}
			ranges = append(ranges, Range{Start: start, End: end})
		} else {
			id, err := strconv.Atoi(line)
			if err != nil {
				return nil, nil, fmt.Errorf("invalid available ID: %s", line)
			}
			ids = append(ids, id)
		}
	}

	if err := scanner.Err(); err != nil {
		return nil, nil, fmt.Errorf("error reading file: %w", err)
	}

	return ranges, ids, nil
}

func solvePuzzle1(ranges []Range, availableIDs []int) int {
	freshCount := 0
	for _, id := range availableIDs {
		isFresh := false
		for _, r := range ranges {
			if r.isFresh(id) {
				isFresh = true
				break
			}
		}
		if isFresh {
			freshCount++
		}
	}
	return freshCount
}

func solvePuzzle2(ranges []Range) int {
	if len(ranges) == 0 {
		return 0
	}

	// Simple sort by range start
	for i := 0; i < len(ranges); i++ {
		for j := i + 1; j < len(ranges); j++ {
			if ranges[i].Start > ranges[j].Start {
				ranges[i], ranges[j] = ranges[j], ranges[i]
			}
		}
	}

	mergedRanges := []Range{ranges[0]}
	
	for i := 1; i < len(ranges); i++ {
		lastMerged := &mergedRanges[len(mergedRanges)-1]
		current := ranges[i]

		// Check for overlap or contiguity (inclusive ranges)
		if current.Start <= lastMerged.End+1 {
			if current.End > lastMerged.End {
				lastMerged.End = current.End
			}
		} else {
			mergedRanges = append(mergedRanges, current)
		}
	}

	totalFreshIDs := 0
	for _, r := range mergedRanges {
		// Count is (End - Start + 1)
		totalFreshIDs += (r.End - r.Start + 1)
	}

	return totalFreshIDs
}

func main() {
	startTotal := time.Now()

	ranges, availableIDs, err := parseInput("input.txt")
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		os.Exit(1)
	}

	startP1 := time.Now()
	result1 := solvePuzzle1(ranges, availableIDs)
	_ = time.Since(startP1) // Ignore individual duration

	startP2 := time.Now()
	rangesCopy := make([]Range, len(ranges))
	copy(rangesCopy, ranges)
	result2 := solvePuzzle2(rangesCopy)
	_ = time.Since(startP2) // Ignore individual duration

	durationTotal := time.Since(startTotal)

	fmt.Printf("Puzzle 1: %d\n", result1)
	fmt.Printf("Puzzle 2: %d\n", result2)
	fmt.Printf("Total Duration: %dµs\n", durationTotal.Microseconds())
}