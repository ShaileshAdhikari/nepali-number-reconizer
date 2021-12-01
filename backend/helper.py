import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd
import numpy as np

def get_detail(directory,subset):
    image_dict = {}
    _, dirs, _ = next(os.walk(directory))
    dirs.sort()
    for val in dirs:
        _,d,f = next(os.walk(directory+'/'+val))
        print('We have {} {} images for {}'.format(len(f),subset,val))
        image_dict[val]=f
    return image_dict

def plot33(DIR,img):
    f, axarr = plt.subplots(3,3)
    axarr[0,0].imshow(mpimg.imread(DIR+'/0/'+img['0'][0]))
    axarr[0,1].imshow(mpimg.imread(DIR+'/1/'+img['1'][0]))
    axarr[1,0].imshow(mpimg.imread(DIR+'/2/'+img['2'][0]))
    axarr[1,1].imshow(mpimg.imread(DIR+'/3/'+img['3'][0]))
    axarr[2,0].imshow(mpimg.imread(DIR+'/4/'+img['4'][0]))
    axarr[0,2].imshow(mpimg.imread(DIR+'/5/'+img['5'][0]))
    axarr[2,1].imshow(mpimg.imread(DIR+'/6/'+img['6'][0]))
    axarr[1,2].imshow(mpimg.imread(DIR+'/7/'+img['7'][0]))
    axarr[2,2].imshow(mpimg.imread(DIR+'/8/'+img['8'][0]))
        
def tr_plot(tr_data, start_epoch):
    #Plot the training and validation data
    tacc=tr_data.history['acc']
    tloss=tr_data.history['loss']
    vacc=tr_data.history['val_acc']
    vloss=tr_data.history['val_loss']
    lr = tr_data.history['lr']
    Epoch_count=len(tacc)+ start_epoch
    Epochs=[]
    for i in range (start_epoch ,Epoch_count):
        Epochs.append(i+1)   
    index_loss=np.argmin(vloss)#  this is the epoch with the lowest validation loss
    val_lowest=vloss[index_loss]
    index_acc=np.argmax(vacc)
    acc_highest=vacc[index_acc]
    plt.style.use('fivethirtyeight')
    sc_label='best epoch= '+ str(index_loss+1 +start_epoch)
    vc_label='best epoch= '+ str(index_acc + 1+ start_epoch)
    
    fig,axes=plt.subplots(nrows=1, ncols=2, figsize=(20,8))
    
    axes[0].plot(Epochs,tloss, 'r', label='Training loss')
    axes[0].plot(Epochs,vloss,'g',label='Validation loss' )
    axes[0].scatter(index_loss+1 +start_epoch,val_lowest, s=150, c= 'blue', label=sc_label)
    axes[0].set_title('Training and Validation Loss')
    axes[0].set_xlabel('Epochs')
    axes[0].set_ylabel('Loss')
    axes[0].legend()
    
    axes[1].plot (Epochs,tacc,'r',label= 'Training Accuracy')
    axes[1].plot (Epochs,vacc,'g',label= 'Validation Accuracy')
    axes[1].scatter(index_acc+1 +start_epoch,acc_highest, s=150, c= 'blue', label=vc_label)
    axes[1].set_title('Training and Validation Accuracy')
    axes[1].set_xlabel('Epochs')
    axes[1].set_ylabel('Accuracy')
    axes[1].legend()
        
    plt.tight_layout
    #plt.style.use('fivethirtyeight')
    plt.show()