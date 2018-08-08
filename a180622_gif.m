opengl software

path=['C:/SSRL/May2017/'];
folder='P2016_04_10';
basename='P2016_04_10_ozone_CTR16_00L';



box=[175 345 30 190];
dbi = 245+1;dbj = 122+1;


filename3 = [path folder '/' basename '_scan1.csv'];%CSV file for attenuation corrections
CSV = importdata(filename3,',',1);

looplength=1:size(CSV.data,1);%[1:150];
for Imageindex=looplength
% filename1 = [path folder '/Pilatus/b_mehta_' basename '_scan1_' num2str(Imageindex-1,'%04i') '.raw.pdi'];
% filename2 = [path folder '/Pilatus/b_mehta_' basename '_scan1_' num2str(Imageindex-1,'%04i') '.raw'];  
filename1 = [path folder '/Pilatus/b_mehta_' basename '_scan1_' num2str(Imageindex-1,'%04i') '.raw.pdi'];
filename2 = [path folder '/Pilatus/b_mehta_' basename '_scan1_' num2str(Imageindex-1,'%04i') '.raw'];  

foils= num2str(CSV.data(:,14),'%04d');
l1 = 0.87; l2 = 2.470; l3 = 3.770; l4 = 10.830; %abs
fabsSTO=1./exp(-str2num(foils(:,1))*l1-str2num(foils(:,2))*l2-str2num(foils(:,3))*l3-str2num(foils(:,4))*l4);
fmon=CSV.data(:,6); 


Image = OpenPilatusImage(filename2);
BoxImage = fabsSTO(Imageindex)./fmon(Imageindex).*Image(box(3):box(4),box(1):box(2),:);


figure('WindowStyle','normal','Position',[5 5 280 180])
clims = [0 4];
imagesc(log10(BoxImage),clims)
hold on
plot([dbi-box(1),dbi-box(1)],[dbj-20-box(3),dbj+20-box(3)],':','Color','black','LineWidth',0.5)
plot([dbi-20-box(1),dbi+20-box(1)],[dbj-box(3),dbj-box(3)],':','Color','black','LineWidth',0.5)
hold off
cbar=colorbar; cbar.Label.String = 'Log10(Intensity)'; colormap(jet); axis equal; axis tight; axis xy; xlabel('pixel ii'); ylabel('pixel jj');
title([basename ', image # ' num2str(Imageindex)],'Interpreter','none');

im = frame2im(getframe(gcf()));
%imwrite(imind,cm,[ppd '/180206_SSRL_72' '/PNG/' num2str(Imageindex), '_PNG.png'])  

%[imind, cm] = rgb2ind(im, 256);
[imind, cm] = rgb2ind(im, 256);
%%
%frame_rate=30;
frame_rate=10;

        if Imageindex == looplength(1)
            imwrite(imind,cm,[pwd  '/GIF/' basename '.gif'],'gif', 'Loopcount',Inf,'DelayTime',1/frame_rate);
        else
            imwrite(imind,cm,[pwd '/GIF/' basename '.gif'],'gif','WriteMode','append','DelayTime',1/frame_rate);
        end
        close all

end
     

%end     
%         %%
%         imwrite(imind,cm,[savepath, fname, '/PNG/',fname,'_', num2str(i), '_PNG.png'])  
%         if i == 1
%             imwrite(imind,cm,[savepath, fname, '/',fname,'.gif'],'gif', 'Loopcount',Inf,'DelayTime',1/frame_rate);
%         else
%             imwrite(imind,cm,[savepath, fname, '/',fname,'.gif'],'gif','WriteMode','append','DelayTime',1/frame_rate);
%         end
% 
%         
%         %%
%         %load properties of the simulation and meshgrids
% load([savepath,fname,'/frameData.mat']);
% load([savepath,fname,'/imageProperties.mat']);
% minX=min(min(X)); minY=min(min(Y));
% maxX=max(max(X)); maxY=max(max(Y));
% 
% %find the available processed Z matricies
% addpath([savepath,fname])
% filelist=ls([savepath,fname,'/*Z.mat']);
% Nfiles=size(filelist,1);%number of files to loop through
% 
% %load in my homemade cmaps choices are teal and red
% myCmaps;
% 
% 
% figure(1);
% h=subplot(1,1,1);
% if save_plots
%     mkdir([savepath, fname, '/PNG'])
% end
% 
% 
% for i=1:Nfiles
%     
%     cla(h);
%     
%     hold off;
%     %load processed Z matrix
%     load([savepath,fname,'/',fname,'_',num2str(i,'%03d'),'Z.mat']);
%     
%     %using image. Z is thresholded and normalized to 255
%     image(X(1,:),Y(:,1),min(Z,N_inject/Contrast)/(N_inject/Contrast)*255);
%     set(gca,'ydir','normal')
%     hold on
%     
%     %plot the frame and ohmics for visual reference
%     plotFrameGroup(frmgrp);
%     
%     %use cmap of your choice
%     colormap(cmap.red);
%     
%     drawnow();
%     if save_plots
%         
%         im = frame2im(getframe(gcf()));
%         [imind, cm] = rgb2ind(im, 256);
%         imwrite(imind,cm,[savepath, fname, '/PNG/',fname,'_', num2str(i), '_PNG.png'])  
%         if i == 1
%             imwrite(imind,cm,[savepath, fname, '/',fname,'.gif'],'gif', 'Loopcount',Inf,'DelayTime',1/frame_rate);
%         else
%             imwrite(imind,cm,[savepath, fname, '/',fname,'.gif'],'gif','WriteMode','append','DelayTime',1/frame_rate);
%         end
%         
%     end
% end
