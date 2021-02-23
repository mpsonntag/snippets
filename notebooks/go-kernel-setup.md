# golang jupyter notebook

This is a quick guide to set up the golang kernel for jupyter notebooks.

```bash
# fetch the latest gophernotes code; will be downloaded to the $GOPATH/src location
go get github.com/gopherdata/gophernotes
# prepare jupyter to use the installed kernel
mkdir -p ~/.local/share/jupyter/kernels/gophernotes
cp $GOPATH/src/github.com/gopherdata/gophernotes/kernel/* ~/.local/share/jupyter/kernels/gophernotes
cd ~/.local/share/jupyter/kernels/gophernotes
chmod +w ./kernel.json
sed "s|gophernotes|$(go env GOPATH)/bin/gophernotes|" < kernel.json.in > kernel.json
```

jupyter should now be able to run a notebook using a go kernel.

