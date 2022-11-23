"""This experiment is for connecting Google Colab to a server running on NSF-supported cloud computing infrastructure. 

This allows you to run experiments requiring bare metal access, storage, memory, GPU and compute that exceeds the abilities of Colab's hosted runtime, but with Colab's familiar interface (and notebooks stored in your Google Drive). It also allows you to easily go back and forth between the convenience of Colab's hosted runtime and Chameleon or CloudLab's greater capabilities, as you develop your experiment.

Instructions:
Wait for the experiment to start, and open a shell on the server. Run:

```
sudo apt update; sudo apt -y install python3-dev jupyter-core jupyter-client python3-pip
```

and

```
python3 -m pip install --user jupyter-core jupyter-client jupyter_http_over_ws traitlets -U --force-reinstall
```

Then start the Jupyter server with

```
PATH="$HOME/.local/bin:$PATH"
jupyter serverextension enable --py jupyter_http_over_ws
jupyter notebook --NotebookApp.allow_origin='https://colab.research.google.com' --port=8888 --NotebookApp.port_retries=0
```

Leave this running, and copy the URL that includes the word "localhost" in it from the output of this command.

Then, from List View, get the SSH login details for the server. In a **local** terminal, run:

```
ssh -L 127.0.0.1:8888:127.0.0.1:8888 ffund00@c240g5-110217.wisc.cloudlab.us
```

(substituting your SSH login for the last part!) Leave this SSH session open.

Now, you can open Colab in a browser. Click on the drop-down menu for "Connect" in the top right and select "Connect to a local runtime".  Past the URL into the space and click "Connect".
"""

# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as pg
# Emulab specific extensions.
import geni.rspec.emulab as emulab

# Create a portal context, needed to defined parameters
pc = portal.Context()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()

osImage = "urn:publicid:IDN+emulab.net+image+emulab-ops//CENTOS8S-64-STD"

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
                   portal.ParameterType.STRING,"/mydata",advanced=True,
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

node = request.RawPC('colab')
node.disk_image = osImage

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



# Print the RSpec to the enclosing page.
pc.printRequestRSpec(request)
