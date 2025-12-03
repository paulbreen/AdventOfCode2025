use std::fs;
use std::io;
use std::time::Instant;

/// Read input.txt as a list of non-empty lines.
fn read_input(path: &str) -> io::Result<Vec<String>> {
    let content = fs::read_to_string(path)?;
    let lines = content
        .lines()
        .map(str::trim)
        .filter(|l| !l.is_empty())
        .map(|s| s.to_string())
        .collect();
    Ok(lines)
}

/// Compute the lexicographically largest subsequence of digits of fixed length k,
/// preserving original order, and return it as an integer.
///
/// Example:
///   line = "234234234234278", k = 2  -> 78
///   line = "234234234234278", k = 12 -> 434234234278
fn max_subseq_value(line: &str, k: usize) -> u64 {
    // Extract digits as numbers 0-9.
    let digits: Vec<u8> = line
        .bytes()
        .filter(|b| b.is_ascii_digit())
        .map(|b| b - b'0')
        .collect();

    let n = digits.len();
    if k == 0 || n == 0 {
        return 0;
    }
    if k >= n {
        // Use all digits.
        let mut val: u64 = 0;
        for d in digits {
            val = val * 10 + d as u64;
        }
        return val;
    }

    let mut remove_left = n - k;
    let mut stack: Vec<u8> = Vec::with_capacity(k);

    for (i, &d) in digits.iter().enumerate() {
        // Greedy: drop smaller previous digits if we can still fill k slots later.
        while let Some(&last) = stack.last() {
            if remove_left > 0 && last < d && (stack.len() - 1 + (n - i)) >= k {
                stack.pop();
                remove_left -= 1;
            } else {
                break;
            }
        }

        if stack.len() < k {
            stack.push(d);
        } else if remove_left > 0 {
            // We must discard some digits overall; if stack is already full, this one is discarded.
            remove_left -= 1;
        }
    }

    // Convert resulting subsequence into an integer.
    let mut val: u64 = 0;
    for d in stack.iter().take(k) {
        val = val * 10 + (*d as u64);
    }
    val
}

/// Puzzle 1: choose exactly 2 digits per bank to maximize the resulting 2-digit number
/// (order preserved), then sum over banks.
fn solve_puzzle1(lines: &[String]) -> u64 {
    lines.iter().map(|line| max_subseq_value(line, 2)).sum()
}

/// Puzzle 2: choose exactly 12 digits per bank to maximize the resulting 12-digit number
/// (order preserved), then sum over banks.
fn solve_puzzle2(lines: &[String]) -> u64 {
    lines.iter().map(|line| max_subseq_value(line, 12)).sum()
}

fn main() {
    let lines = match read_input("input.txt") {
        Ok(lines) => lines,
        Err(e) => {
            eprintln!("Error: could not read 'input.txt': {}", e);
            std::process::exit(1);
        }
    };

    let start = Instant::now();
    let p1 = solve_puzzle1(&lines);
    let mid = Instant::now();
    let p2 = solve_puzzle2(&lines);
    let end = Instant::now();

    // Times are measured separately but only total duration is printed, per spec.
    let _p1_ms = (mid - start).as_secs_f64() * 1000.0;
    let _p2_ms = (end - mid).as_secs_f64() * 1000.0;
    let total_ms = (end - start).as_secs_f64() * 1000.0;

    println!("Puzzle 1: {}", p1);
    println!("Puzzle 2: {}", p2);
    println!("Total Duration: {:.3}ms", total_ms);
}
