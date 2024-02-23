# RSA Message Signing and Verification

This repository contains a Python program for signing and verifying messages using RSA encryption.

## Setup

To run the program, ensure you have Python 3 installed on your system.

## Usage

### Generating RSA Keys

To generate RSA key pairs, execute the following command:

```bash
python3 *.py 1
```

Alternatively, you can use:

```bash
make run
```

This will create two files:
- `e_n.csv`: Public key
- `d_n.csv`: Private key

### Signing a Message

To sign a message, execute the following command:

```bash
python3 *.py 2 s message.txt
```

Or using the make command:

```bash
make run2 MESSAGE=message.txt
```

This will create a file named `message.txt.signed` which includes the original message along with the encrypted signature.

### Verifying a Signature

To verify a signature, execute the following command:

```bash
python3 *.py 2 v message.txt.signed
```

Or using the make command:

```bash
make run2v MESSAGE=message.txt.signed
```

This will verify the signature against the content of the file and output whether the signature is valid or not.

## File Structure

- `README.md`: Instructions and information about the repository.
- `*.py`: Python scripts for generating keys, signing, and verifying messages.
- `message.txt`: Text file containing the message to be signed.
- `e_n.csv`: CSV file containing the public key.
- `d_n.csv`: CSV file containing the private key.
- `message.txt.signed`: File containing the original message with the encrypted signature.

## Notes

- Ensure you have proper permissions set up to execute the Python scripts.
- Make sure to have all necessary dependencies installed.

Please feel free to contribute or report issues!