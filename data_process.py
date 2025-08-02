import json
import random
import argparse
import os

def main():
    # Argument parser for flexible usage
    parser = argparse.ArgumentParser(description="Process large Amazon review JSON file and create a smaller random sample.")
    parser.add_argument("--input", default="Books.json", help="Input JSON file inside ./data/ directory")
    parser.add_argument("--output", default="Books_small.json", help="Output JSON file inside ./data/ directory")
    parser.add_argument("--year", type=int, default=2014, help="Year to filter reviews by")
    parser.add_argument("--sample_size", type=int, default=1000, help="Number of random reviews to keep")
    args = parser.parse_args()

    # Define file paths
    input_path = os.path.join("data", args.input)
    output_path = os.path.join("data", args.output)

    print(f"📂 Reading from: {input_path}")
    print(f"💾 Will save to: {output_path}")
    print(f"📅 Filtering reviews from year: {args.year}")
    print(f"🎯 Random sample size: {args.sample_size}")

    # Check if input file exists
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"❌ Input file {input_path} not found!")

    filtered_reviews = []

    # Load and filter reviews
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                review = json.loads(line)
                if 'reviewTime' not in review:
                    continue
                year = int(review['reviewTime'].split()[-1])
                if year == args.year:
                    filtered_reviews.append(review)
            except Exception as e:
                print(f"⚠️ Skipping line due to error: {e}")
                continue

    print(f"✅ Total reviews from year {args.year}: {len(filtered_reviews)}")

    # Sample the reviews randomly
    sample_size = min(args.sample_size, len(filtered_reviews))
    sampled_reviews = random.sample(filtered_reviews, sample_size)

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Write sampled reviews to output file
    with open(output_path, 'w', encoding='utf-8') as f:
        for review in sampled_reviews:
            f.write(json.dumps(review) + '\n')

    print(f"🎉 Done! Saved {sample_size} reviews to: {output_path}")

if __name__ == "__main__":
    main()
