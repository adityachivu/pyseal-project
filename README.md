# seal-project
Project using PySEAL for Data Security and Ethics course

## Installing PySEAL
* clone [PySEAL](https://github.com/Lab41/PySEAL)
* `cd PySEAL`
* `sudo ./build-docker.sh`

## Setting up this repo
* clone [`pyseal-project`](https://github.com/adityachivu/pyseal-project)

## Running with persistent storage volume
* `cd ~/seal-project`
* `sudo docker run -v /absolute/path/:/seal-project/ -w /seal-project/ -it seal bash`

# Progress Report - Jun 7th

* Installed PySEAL library and ran sample scripts, (but only with docker).
* Began reading FV encryption scheme off which the library is based on.

As per understanding:

The encryption scheme requires some manually set parameters. Of these, the most important/relevant is the 
cipherrtextmodulus. This determines the `noise budget` for any calculation of a homomorphically encrypted entity.
The documentation states that the every computation `consumes` some of the noise budget and exceeding the budget would
cause the result to lose its integrity.

### Important Considerations
* Clear delineation between *data owner* and *data processor*, i.e. the data processing agent should only be able to
see the encrypted data and perform operations on it.

* For a matrix-matrix multiplication. We would consume some noise budget for every multiplication operation performed.
Since the number of operations for which a specific element x_ij would depend on the size of the second matrix. UPDATE:
noise budget consumed w.r.t multiplicative depth. Not number of multiplications. As depth=2 for any given
matrix multiplication, noise budget is not an issue for matrix multiplication. However, cascading of matrix multuiplication
would increase the multiplicative depth correspondingly. (#TODO:Verify with arbitrary vector sizes)


### Processing steps
1. Create and set paramteres

2. create context

3. 


# Progress Report - Jun 21st

* Implemented dot product of floats for fixed length arrays using list of ciphertext.

* Defined custom `CipherMatrix class` which is a numpy matrix of Ciphertext objects. dynamically created when custom
encrypt function is called.

* Defined pickle based file readers and writers for storing encrypted matrices to file. The purpose of this is to allow
an external "server" script to read the file, perform the homomorphically encrypted matrix multiplication and store the
result back in the same file.

# TODO

* Adapt pickle files to include context parameters for 'server' script to generate evaluator object from.

* Documentation of SEAL workflow.

* Saved Trained MNIST model for 2-layer feedforward network 

