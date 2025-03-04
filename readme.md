# Stitch Fix

The other day i ran into someone who built software to take your measurements for custom suits. You would
take a picture of yourself and the software would take your measurements. I thought that was pretty cool.
So naturally, I wanted to build something similar. I wanted to build something that would take your
measurements but it would then generate sewing patterns for you. I thought that would be pretty cool.

> [!WARNING]  
> This is a work in progress. I am still working on this project. I will update this page as I make progress.

## Prerequisites
- Python 3.6 or higher

## Installation

1. Clone the repository
```bash
git clone https://github.com/conceptcodes/stitch-fix.git
cd stitch-fix
```

2. Install the dependencies
```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py -i <image_path> -g <garment> -o <output_path>
```