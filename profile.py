# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as pg
# Emulab specific extensions.
import geni.rspec.emulab as emulab
# for tour, instructions
import geni.rspec.igext as ig


# Create a portal context, needed to defined parameters
pc = portal.Context()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()

# Pick your OS.
imageList = [
    ('urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD', 'UBUNTU 22.04'),
    ('urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU20-64-STD', 'UBUNTU 20.04')]

pc.defineParameter("osImage", "Select OS image",
                   portal.ParameterType.IMAGE,
                   imageList[0], imageList,
                   longDescription="Select a disk image.")

#    'c240g5', 'c240g5',  # 32 at Wisconsin
#    'c4130', 'c4130',    # 2 at Wisconsin, 2 at Clemson
#    'r7525', 'r7525'     # 15 at Clemson



# Optional physical type for all nodes.
pc.defineParameter("phystype",  "Physical node type",
                   portal.ParameterType.STRING, "",
                   longDescription="Specify a physical node type (c240g5, c4130, r7525) " +
                   "instead of letting the resource mapper choose for you.")

# Optional ephemeral blockstore
pc.defineParameter("tempFileSystemSize", "Temporary Filesystem Size",
                   portal.ParameterType.INTEGER, 0,advanced=True,
                   longDescription="The size in GB of a temporary file system to mount on each of your " +
                   "nodes. Temporary means that they are deleted when your experiment is terminated. " +
                   "The images provided by the system have small root partitions, so use this option " +
                   "if you expect you will need more space to build your software packages or store " +
                   "temporary files.")
                   
# Instead of a size, ask for all available space. 
pc.defineParameter("tempFileSystemMax",  "Temp Filesystem Max Space",
                    portal.ParameterType.BOOLEAN, True,
                    advanced=True,
                    longDescription="Instead of specifying a size for your temporary filesystem, " +
                    "check this box to allocate all available disk space. Leave the size above as zero.")

pc.defineParameter("tempFileSystemMount", "Temporary Filesystem Mount Point",
                   portal.ParameterType.STRING,"/data",advanced=True,
                   longDescription="Mount the temporary file system at this mount point; in general you " +
                   "you do not need to change this, but we provide the option just in case your software " +
                   "is finicky.")

# Retrieve the values the user specifies during instantiation.
params = pc.bindParameters()

# Check parameter validity.
if params.tempFileSystemSize < 0 or params.tempFileSystemSize > 200:
    pc.reportError(portal.ParameterError("Please specify a size greater then zero and " +
                                         "less then 200GB", ["nodeCount"]))

pc.verifyParameters()

ubuntuInstructions = """

The automated install process, which installs GPU drivers, CUDA, and some machine learning libraries, will take a while.

After the automated install process is complete (you should see a check mark in the corner of the node), reboot the node to load the newly installed driver:

```
sudo reboot
```

Wait for the resource to come back up.

This host has a large filesystem available at `/data` - run

```
sudo chown $USER /data
```

so that you will be able to write to this filesystem. 

You can then install any additional Python packages, but use e.g.

```
TMPDIR=/data/tmp python3 -m pip install --cache-dir=/data/tmp --target=/data XXX
```

to install a package named `XXX` - there is not enough disk space on the root filesystem.

Then, start the notebook server:

```
PATH="/data/bin:$PATH"
cd /data
PYTHONPATH=/data jupyter server extension enable --py jupyter_http_over_ws
PYTHONPATH=/data jupyter notebook --notebook-dir=/data --NotebookApp.allow_origin='https://colab.research.google.com' --port=8888 --NotebookApp.port_retries=0
```

In the output, look for a URL in this format:
    
```
http://localhost:8888/?token=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

and copy it.

Then, from List View, get the SSH login details for the server. In a local terminal, run:

```
ssh -L 127.0.0.1:8888:127.0.0.1:8888 USER@{host-colab}
```

(substituting your CloudLab username in place of `USER`! Also specify your key path using `-i`, if it is not in the default location.) Leave this SSH session open.

Now, you can open Colab in a browser. Click on the drop-down menu for "Connect" in the top right and select "Connect to a local runtime". Paste the URL into the space and click "Connect".

"""

ubuntu22Instructions = """

The automated install process, which installs GPU drivers, CUDA, and some machine learning libraries, will take a while.

After the automated install process is complete (you should see a check mark in the corner of the node), reboot the node to load the newly installed driver:

```
sudo reboot
```

Wait for the resource to come back up.

This host has a large filesystem available at `/data` - run

```
sudo chown $USER /data
```

so that you will be able to write to this filesystem. 

Next, install Python packages:

```
mkdir -p /data/tmp
sudo chown $USER -R /data

TMPDIR=/data/tmp python3 -m pip install --user --cache-dir=/data/tmp Cython==3.0.5
TMPDIR=/data/tmp python3 -m pip install --user --cache-dir=/data/tmp -r /local/repository/requirements_cloudlab_dl22.txt --extra-index-url https://download.pytorch.org/whl/cu118 -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html
TMPDIR=/data/tmp python3 -m pip install --user --cache-dir=/data/tmp  jupyter-core==5.5.0 jupyter-client==6.1.12 jupyter-server==1.24.0 jupyterlab-widgets==3.0.9  jupyterlab==3.6.6 jupyter_http_over_ws traitlets 
```

Then, start the notebook server:

```
PATH="/$HOME/.local/bin:$PATH"

jupyter server extension enable --py jupyter_http_over_ws
jupyter notebook --notebook-dir=/data --NotebookApp.allow_origin='https://colab.research.google.com' --port=8888 --NotebookApp.port_retries=0
```

In the output, look for a URL in this format:
    
```
http://localhost:8888/?token=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

and copy it.

Then, from List View, get the SSH login details for the server. In a local terminal, run:

```
ssh -L 127.0.0.1:8888:127.0.0.1:8888 USER@{host-colab}
```

(substituting your CloudLab username in place of `USER`! Also specify your key path using `-i`, if it is not in the default location.) Leave this SSH session open.

Now, you can open Colab in a browser. Click on the drop-down menu for "Connect" in the top right and select "Connect to a local runtime". Paste the URL into the space and click "Connect".

"""


centosInstructions = ubuntuInstructions

tourDescription = """
This experiment is for connecting Google Colab to a server running on NSF-supported cloud computing infrastructure.

This allows you to run experiments requiring bare metal access, storage, memory, GPU and compute that exceeds the abilities of Colab's hosted runtime, but with Colab's familiar interface (and notebooks stored in your Google Drive). It also allows you to easily go back and forth between the convenience of Colab's hosted runtime and Chameleon or CloudLab's greater capabilities, as you develop your experiment.
"""

node = request.RawPC('colab')
node.disk_image = params.osImage

# Optional hardware type.
if params.phystype != "":
  node.hardware_type = params.phystype

# Optional Blockstore
if params.tempFileSystemSize > 0 or params.tempFileSystemMax:
    bs = node.Blockstore("colab-bs", params.tempFileSystemMount)
    if params.tempFileSystemMax:
        bs.size = "0GB"
    else:
      bs.size = str(params.tempFileSystemSize) + "GB"
    bs.placement = "any"


if params.osImage and params.osImage.endswith('UBUNTU20-64-STD'):
    node.addService(pg.Execute(shell="bash", command="/bin/bash /local/repository/cloudlab-ubuntu-install.sh"))
    tourInstructions = ubuntuInstructions
elif params.osImage and params.osImage.endswith('UBUNTU22-64-STD'):
    node.addService(pg.Execute(shell="bash", command="/bin/bash /local/repository/cloudlab-ubuntu-install.sh"))
    tourInstructions = ubuntu22Instructions
else:
  tourInstructions = ""


tour = ig.Tour()
tour.Description(ig.Tour.TEXT,tourDescription)
tour.Instructions(ig.Tour.MARKDOWN,tourInstructions)
request.addTour(tour)

# Print the RSpec to the enclosing page.
pc.printRequestRSpec(request)
