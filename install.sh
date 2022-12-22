# install minimap
git clone https://github.com/lh3/minimap2
cd minimap2 && make
cd ..

#install samtools
wget https://github.com/samtools/samtools/releases/download/1.9/samtools-1.9.tar.bz2
tar -vxjf samtools-1.9.tar.bz2
cd samtools-1.9
make
cd ..

