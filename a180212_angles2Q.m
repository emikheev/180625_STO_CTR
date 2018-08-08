function [H,K,L]=a180212_angles2Q(th,tth,chi,phi,dtth,dgamma,wavevector,a,b,c,box)

t1=(th).*pi/180;
t2=(chi-90).*pi/180;
t3=(180-phi).*pi/180;
t4=(dgamma).*pi/180;
t5=(tth+dtth).*pi/180;


%From a18012_sym.m
%Qi=eye(3)/U/Rzphi/Rychi/Rxth*(Rxtth*Rzgamma-eye(3))*Wavevector;
%Q=[a;b;c]./2./pi.*Qi;


H_temp=(a.*wavevector.*(((cos(t4).*cos(t5) - 1).*(cos(t3).*sin(t1).*sin(t2) + cos(t1).*cos(t2)^2.*sin(t3) + cos(t1).*sin(t2)^2.*sin(t3)))/((cos(t1)^2 + sin(t1)^2).*(cos(t2)^2 + sin(t2)^2).*(cos(t3)^2 + sin(t3)^2)) - (cos(t2).*cos(t3).*sin(t4))/((cos(t2)^2 + sin(t2)^2).*(cos(t3)^2 + sin(t3)^2)) + (cos(t4).*sin(t5).*(cos(t2)^2.*sin(t1).*sin(t3) + sin(t1).*sin(t2)^2.*sin(t3) - cos(t1).*cos(t3).*sin(t2)))/((cos(t1)^2 + sin(t1)^2).*(cos(t2)^2 + sin(t2)^2).*(cos(t3)^2 + sin(t3)^2))))/(2.*pi);
K_temp=(b.*wavevector.*((cos(t2).*sin(t3).*sin(t4))/((cos(t2)^2 + sin(t2)^2).*(cos(t3)^2 + sin(t3)^2)) + ((cos(t4).*cos(t5) - 1).*(cos(t1).*cos(t2)^2.*cos(t3) - sin(t1).*sin(t2).*sin(t3) + cos(t1).*cos(t3).*sin(t2)^2))/((cos(t1)^2 + sin(t1)^2).*(cos(t2)^2 + sin(t2)^2).*(cos(t3)^2 + sin(t3)^2)) + (cos(t4).*sin(t5).*(cos(t1).*sin(t2).*sin(t3) + cos(t2)^2.*cos(t3).*sin(t1) + cos(t3).*sin(t1).*sin(t2)^2))/((cos(t1)^2 + sin(t1)^2).*(cos(t2)^2 + sin(t2)^2).*(cos(t3)^2 + sin(t3)^2))))/(2.*pi);
L_temp=-(c.*wavevector.*((sin(t2).*sin(t4))/(cos(t2)^2 + sin(t2)^2) + (cos(t2).*sin(t1).*(cos(t4).*cos(t5) - 1))/((cos(t1)^2 + sin(t1)^2).*(cos(t2)^2 + sin(t2)^2)) - (cos(t1).*cos(t2).*cos(t4).*sin(t5))/((cos(t1)^2 + sin(t1)^2).*(cos(t2)^2 + sin(t2)^2))))/(2.*pi);


H = zeros(195,487); K = zeros(195,487); L = zeros(195,487);
H(box(3):box(4),box(1):box(2))=H_temp;
K(box(3):box(4),box(1):box(2))=K_temp;
L(box(3):box(4),box(1):box(2))=L_temp;


end