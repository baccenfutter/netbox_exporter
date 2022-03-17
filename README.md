# Netbox-Exporter

*Netbox-Exporter* is a Python package and CLI utility for fetching a Netbox inventory and dumping it to a local directory in YAML format for human consumption.

## Getting started

## Installation

```
pip install netbox_exporter
```

## Usage

```
# netbox_exporter --help

# netbox_export \
    --dir ./netbox \
    --url https://netbox \
    --apikey 0123456789abcdef
```

## Development

```
pipenv install --dev
```