clear all

path=['C:/SSRL/May2017/'];
folder='P2016_04_10';
ii=1;basename='P2016_04_10_ozone_CTR16_00L';STOtHKL=[0,0,2];
%ii=2;basename='P2016_04_10_ozone_CTR21_00L';STOtHKL=[0,0,2];

tic
makeplots='yes';
makeps='no';
options=  optimset('display','off');
opengl software

if strcmp(makeps,'yes')
    filename4 = [pwd '/print/180625_6_3K']; %
end


a=3.905; b=a;c=a;%STO lattice at RT

box=[175 345 30 190];
for cycle=1%:2
    
    
    
    
    Wi=20;Lj=20;%WROI=1+2*wi pixels%LROI=1+2*Lj pixels
    Wi2=5;Lj2=5;
    %standard direct beam pixel
    dbi = 245+1;dbj = 122+1;
    ci=dbi;cj=dbj;
    %non-standard ROI center
    %ci = dbi+1;cj = dbj+1;
    
    %a180324_ROI_exceptions
    
    
    filename3 = [path folder '/' basename '_scan1.csv'];%CSV file for attenuation corrections
    CSV = importdata(filename3,',',1);
    foils= num2str(CSV.data(:,14),'%04d');
    l1 = 0.87; l2 = 2.470; l3 = 3.770; l4 = 10.830; %abs
    fabsSTO=1./exp(-str2num(foils(:,1))*l1-str2num(foils(:,2))*l2-str2num(foils(:,3))*l3-str2num(foils(:,4))*l4);
    w = 172; %pixel width = 172 microns, ii = 1-487 pixels, jj = 1-195 pixels
    R = 1.145*1e6; %detector-diffractometer center, in microns
    
    fmon=CSV.data(:,6);
    
    ROIbox = [ci-Wi ci+Wi cj-Lj cj+Lj]; % ii bottom, iitop, jj bottom, top
    
    for Imageindex=1:size(CSV.data,1)
        %filename1 = [path folder '/Pilatus/b_mehta_' basename '_scan1_' num2str(Imageindex-1,'%04i') '.raw.pdi'];
        %filename2 = [path folder '/Pilatus/b_mehta_' basename '_scan1_' num2str(Imageindex-1,'%04i') '.raw'];
        
        filename1 = [path 'PilatusAll/b_mehta_' basename '_scan1_' num2str(Imageindex-1,'%04i') '.raw.pdi'];
        filename2 = [path 'PilatusAll/b_mehta_' basename '_scan1_' num2str(Imageindex-1,'%04i') '.raw'];
    Image = OpenPilatusImage(filename2);
        %fabs=1./exp(-str2num(foils(STOImageindex,1))*l1-str2num(foils(STOImageindex,2))*l2-str2num(foils(STOImageindex,3))*l3-str2num(foils(STOImageindex,4))*l4);
        [angles,lambda] = PDI_Imp(filename1);
        wavevector = 2*pi / lambda; %A^-1
        Wavevector=[0;wavevector;0];
        th = angles(1);
        tth = angles(2);
        chi = angles(3);
        phi=-2.947;
        [II,JJ]=meshgrid(box(1):box(2),box(3):box(4));
        dtth=-atan((dbi-II)*w/R)*180/pi;
        dgamma=atan((dbj-JJ)*w/R)*180/pi;
        [h,k,l]=a180212_angles2Q(th,tth,chi,phi,dtth,dgamma,wavevector,a,b,c,box);
        
        if cycle == 1
            H(:,:,Imageindex)=h;
            K(:,:,Imageindex)=k;
            L(:,:,Imageindex)=l;
        elseif cycle == 2
            H(:,:,Imageindex)=h-dH;
            K(:,:,Imageindex)=k-dK;
            L(:,:,Imageindex)=l-dL;
        end
        
        ROIImage = Image(ROIbox(3):ROIbox(4),ROIbox(1):ROIbox(2),:);
        ROIraw(Imageindex)=mean(mean(ROIImage));
        ROI(Imageindex)=fabsSTO(Imageindex)./fmon(Imageindex).*mean(mean(ROIImage));
        dbInt(Imageindex) = fabsSTO(Imageindex)./fmon(Imageindex).*Image(dbj,dbi,:);
        
    end
    
    
    H1=squeeze(H(dbj,dbi,:));
    K1=squeeze(K(dbj,dbi,:));
    L1=squeeze(L(dbj,dbi,:));
    
    
    
    
    
    
    
    [~,maxImageindex]=max(ROI);
    filename2 = [path folder '/Pilatus/b_mehta_' basename '_scan1_' num2str(maxImageindex-1,'%04i') '.raw'];
    Image = OpenPilatusImage(filename2);
    BoxImage = Image(box(3):box(4),box(1):box(2),:);
    [Max,Loc]=max(BoxImage(:));
    [c2j,c2i]=ind2sub(size(BoxImage),Loc);
    c2j=c2j+box(3)-1;c2i=c2i+box(1)-1;
    ROIbox2 = [c2i-Wi2 c2i+Wi2 c2j-Lj2 c2j+Lj2];
    
    for Imageindex=1:size(CSV.data,1)
        filename1 = [path folder '/Pilatus/b_mehta_' basename '_scan1_' num2str(Imageindex-1,'%04i') '.raw.pdi'];
        filename2 = [path folder '/Pilatus/b_mehta_' basename '_scan1_' num2str(Imageindex-1,'%04i') '.raw'];
        Image = OpenPilatusImage(filename2);
        [angles,lambda] = PDI_Imp(filename1);
        wavevector = 2*pi / lambda;Wavevector=[0;wavevector;0];
        th = angles(1); tth = angles(2); chi = angles(3); phi = -5.517;
        [II,JJ]=meshgrid(box(1):box(2),box(3):box(4));
        dtth=-atan((dbi-II)*w/R)*180/pi;
        dgamma=atan((dbj-JJ)*w/R)*180/pi;
        [h,k,l]=a180212_angles2Q(th,tth,chi,phi,dtth,dgamma,wavevector,a,b,c,box);
        
        if cycle == 1
            H(:,:,Imageindex)=h;
            K(:,:,Imageindex)=k;
            L(:,:,Imageindex)=l;
        elseif cycle == 2
            H(:,:,Imageindex)=h-dH;
            K(:,:,Imageindex)=k-dK;
            L(:,:,Imageindex)=l-dL;
        end
        
        
        H2=squeeze(H(c2j,c2i,:));
        K2=squeeze(K(c2j,c2i,:));
        L2=squeeze(L(c2j,c2i,:));
        
        
        
        
        ROIImage2 = Image(ROIbox2(3):ROIbox2(4),ROIbox2(1):ROIbox2(2),:);
        ROI2(Imageindex)=fabsSTO(Imageindex)./fmon(Imageindex).*mean(mean(ROIImage2));
    end
    
    [~,maxImageindex2]=max(ROI2);
    filename2 = [path folder '/Pilatus/b_mehta_' basename '_scan1_' num2str(maxImageindex2-1,'%04i') '.raw'];
    Image = OpenPilatusImage(filename2);
    BoxImage = Image(box(3):box(4),box(1):box(2),:);
    [maxROI2,~]=max(ROI2);
    
    
    
    if cycle == 1
        
        dH=H2(maxImageindex2)-STOtHKL(1);
        dK=K2(maxImageindex2)-STOtHKL(2);
        dL=L2(maxImageindex2)-STOtHKL(3);
    end
    %
    %     %%
    %     if strcmp(peaktype,'STO')
    %     save1(ii).STOmaxImageindex2 = maxImageindex2;
    %     save1(ii).dH=H2(maxImageindex2)-save1(ii).STOtHKL(1);
    %     save1(ii).dK=K2(maxImageindex2)-save1(ii).STOtHKL(2);
    %     save1(ii).dL=L2(maxImageindex2)-save1(ii).STOtHKL(3);
    %
    %     save1(ii).HSTO=H2(maxImageindex2);
    %     save1(ii).KSTO=K2(maxImageindex2);
    %     save1(ii).LSTO=L2(maxImageindex2);
    %
    %     if save1(ii).STOtHKL(1) ~= 0
    %         save1(ii).mHSTO=H2(maxImageindex2)./save1(ii).STOtHKL(1);
    %     else
    %         save1(ii).mHSTO=0;
    %     end
    %     if save1(ii).STOtHKL(2) ~= 0
    %         save1(ii).mKSTO=K2(maxImageindex2)./save1(ii).STOtHKL(2);
    %     else
    %         save1(ii).mKSTO=0;
    %     end
    %     save1(ii).mLSTO=L2(maxImageindex2)./save1(ii).STOtHKL(3);
    %
    %     save1(ii).c2imaxSTO=c2i;
    %     save1(ii).c2jmaxSTO=c2j;
    %     save1(ii).maxROI2STO=maxROI2;
    %     end
    %
    %     if strcmp(peaktype,'BPBO')
    %     save1(ii).BPBOmaxImageindex2 = maxImageindex2;
    %     save1(ii).HBPBO=H2(maxImageindex2);%./save1(ii).BPBOtHKL(1);
    %     save1(ii).KBPBO=K2(maxImageindex2);%./save1(ii).BPBOtHKL(1);
    %     save1(ii).LBPBO=L2(maxImageindex2);%./save1(ii).BPBOtHKL(1);
    %
    %
    %     if save1(ii).BPBOtHKL(1) ~= 0
    %         save1(ii).mHBPBO=save1(ii).HBPBO./save1(ii).BPBOtHKL(1);
    %     else
    %         save1(ii).mHBPBO=0;
    %     end
    %     if save1(ii).BPBOtHKL(2) ~= 0
    %         save1(ii).mKBPBO=save1(ii).KBPBO./save1(ii).BPBOtHKL(2);
    %     else
    %         save1(ii).mKBPBO=0;
    %     end
    %
    %     save1(ii).mLBPBO=save1(ii).LBPBO./save1(ii).BPBOtHKL(3);
    %
    %     save1(ii).maxROI2=maxROI2;
    %
    %
    %     end
    
    %%
    if strcmp(makeplots,'yes')
        
        if cycle == 1
            Fig=figure;
            set(Fig,'WindowStyle','docked','PaperOrientation','landscape','PaperType','uslegal');
            
            subplot(211)
            semilogy(L1,dbInt,'k-')
            hold on
            
            semilogy(L1,ROI,'m--')
            semilogy(L2,ROI2,'r.-')
            
            hold off
            legend('at d.b.','large ROI','adjusted small ROI')
            subplot(212)
            filename2 = [path folder '/Pilatus/b_mehta_' basename '_scan1_' num2str(maxImageindex2-1,'%04i') '.raw'];
            Image = OpenPilatusImage(filename2);
            
            clims = [0 4];
            imagesc(log10(Image),clims)
            %text(20,20,[basename ', Image ' num2str(Imageindex,'%02i')],'Color','white','FontWeight','bold','Interpreter','none');
            cbar=colorbar; cbar.Label.String = 'Log10(Intensity)'; colormap(jet); axis equal; xlim([1 487]); ylim([1 195]); xlabel('pixel ii'); ylabel('pixel jj');
            hold on
            % plot(save1(ii).Locii,save1(ii).Locjj,'wO','MarkerSize',5,'LineWidth',1)
            plot([dbi,dbi],[5,190],'--','Color','black','LineWidth',1)
            plot([5,540],[dbj,dbj],'--','Color','black','LineWidth',1)
            plot([ROIbox(1),ROIbox(1)],[ROIbox(3),ROIbox(4)],'--','Color','magenta','LineWidth',1)
            plot([ROIbox(2),ROIbox(2)],[ROIbox(3),ROIbox(4)],'--','Color','magenta','LineWidth',1)
            plot([ROIbox(1),ROIbox(2)],[ROIbox(3),ROIbox(3)],'--','Color','magenta','LineWidth',1)
            plot([ROIbox(1),ROIbox(2)],[ROIbox(4),ROIbox(4)],'--','Color','magenta','LineWidth',1)
            
            plot([ROIbox2(1),ROIbox2(1)],[ROIbox2(3),ROIbox2(4)],'-','Color','red','LineWidth',1)
            plot([ROIbox2(2),ROIbox2(2)],[ROIbox2(3),ROIbox2(4)],'-','Color','red','LineWidth',1)
            plot([ROIbox2(1),ROIbox2(2)],[ROIbox2(3),ROIbox2(3)],'-','Color','red','LineWidth',1)
            plot([ROIbox2(1),ROIbox2(2)],[ROIbox2(4),ROIbox2(4)],'-','Color','red','LineWidth',1)
            
            plot([box(1),box(1)],[box(3),box(4)],'-','Color','k','LineWidth',1)
            plot([box(2),box(2)],[box(3),box(4)],'-','Color','k','LineWidth',1)
            plot([box(1),box(2)],[box(3),box(3)],'-','Color','k','LineWidth',1)
            plot([box(1),box(2)],[box(4),box(4)],'-','Color','k','LineWidth',1)
            
            
            hold off
            title([basename ', Image ' num2str(maxImageindex2-1,'%01i')],'Color','black','FontWeight','bold','Interpreter','none');
        elseif cycle ==2
            subplot(211)
            hold on
            semilogy(L2,ROI2,'k.-')
            legend('at d.b.','large ROI','adjusted small ROI', 'shifted small ROI')
            hold off
        end
        
    end
    
    
    
    
    
    
    
    if strcmp(makeps,'yes')
        print(filename4,'-dpsc','-fillpage','-append')
    end
    
    
end





if strcmp(makeps,'yes')
    
    ps2pdf('psfile', [filename4 '.ps'], 'pdffile', [filename4 '.pdf'], 'gspapersize', 'a4',...
        'gscommand','C:\Program Files\gs\gs9.21\bin\gswin64.exe',...
        'gsfontpath','C:\Program Files\gs\gs9.21\lib',...
        'gslibpath','C:\Program Files\gs\gs9.21\lib');
    
    delete([filename4 '.ps'])
end

toc
toc/60