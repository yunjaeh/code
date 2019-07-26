% function ACH = ACH_concentration_decay(data)
function ACH_local_gradient(data, input_options)
% A function computes air change per hour(ACH) with given concentration
% decay measurement data
%
%   inputs
%       - data input: time
%       - data input: concentration
%       - options
%
%   outputs
%       - figure
%       - min/max (or 95% confidence interval) of ACH
%
%   equation?
%
% modify options

if length(data.time) ~= length(data.c)
    error('Time and concentration data should have consistent length')
end

% options
if(exist('input_options') & ~isempty(input_options))
    if(~exist('input_options.minute_average'))   input_options.minute_average = false;       end
    if(~exist('input_options.smoothing_scheme')) input_options.smoothing_scheme = 'moving';  end
    if(~exist('input_options.smoothing_span'))   input_options.smoothing_span = 31;          end
    if(~exist('input_options.gradient_skip'))    input_options.gradient_skip = 30;          end
    if(~exist('input_options.gradient_span'))    input_options.gradient_span = 10 * 60 / 2 ;          end
    if(~exist('input_options.plot'))             input_options.plot = true;                  end
else
    input_options.minute_average    = false;
    input_options.smoothing_scheme  = 'moving';
    input_options.smoothing_span    = 31;
    input_options.gradient_skip     = 30;
    input_options.gradient_span     = 10 * 60 / 2 ;
    input_options.plot              = true;
end

input_options


TT_raw = timetable(data.time, data.c);

if input_options.minute_average
    TT          = retime(TT_raw,'minutely','mean');
    time_sec    = 60;
    span        = input_options.gradient_span/60;
else
    TT          = TT_raw;
    TT.c        = smooth(TT_raw.Var1,input_options.smoothing_span,...
                    input_options.smoothing_scheme);
    time_sec    = 1;
    span        = input_options.gradient_span;
end




% index of peak concentration
idx_peak    = find(max(TT.c) == TT.c);


c_peak      = min(TT.c(idx_peak));
c_exp       = TT.c(idx_peak+1:end);
del_t       = 1:length(c_exp);

gradient_pt = (idx_peak+span):input_options.gradient_skip:(length(TT.c)-span);
P           = zeros(length(gradient_pt),2);



if input_options.plot
    figure();
    subplot(1,3,1);hold on
    plot(TT_raw.Time,TT_raw.Var1,'color',[0.3 0.3 0.3])
    plot(TT.Time,TT.c,'b','linewidth',2);
    legend('Raw data','Smoothed data')
    legend boxoff
    xlabel('Time'); ylabel('Tracer concentration');
    
    subplot(1,3,2); hold on
    plot(TT.Time,TT.c,'b','linewidth',2);
    plot(TT.Time(gradient_pt), TT.c(gradient_pt),'ko');
    for j= 1:length(gradient_pt)
        c_temp = TT.c(gradient_pt(j) + (-span:span));
        P_temp=fitlm((-span:span),c_temp);
        P(j,:) = P_temp.Coefficients.Estimate;
        plot(TT.Time(gradient_pt(j)+(-span:span)), P(j,2)*(-span:span) + TT.c(gradient_pt(j)),'k');
    end
    xlabel('Time [min]'); ylabel('ACH [1/h]');
    ACH = P(:,2)*-3600/time_sec;
    
    subplot(1,3,3);
    plot(del_t(gradient_pt-idx_peak)*time_sec/60, ACH, 'bo','linewidth',2);
    grid on
    xlabel('Time [min]'); ylabel('ACH [1/h]');
end
    for j= 1:length(gradient_pt)
        c_temp = TT.c(gradient_pt(j) + (-span:span));
        P_temp=fitlm((-span:span),c_temp);
        P(j,:) = P_temp.Coefficients.Estimate;
    end
    ACH = P(:,2)*-3600/time_sec;

end



%     figure(105);
%     subplot(3,4,i); hold on
%     plot((1:len_data)/60, TT.Var1);
%     plot([idx_start idx_start]/60,[0 20],'k--');
%     plot([idx_start+600 idx_start+600]/60,[0 20],'k--');
%     ylim([0 10]);
%     title(config);
%     
%     P = zeros(len_data,2);
%     for j=idx_start:1:(len_data-span)
%         c_temp = TT.Var1(j + (-span:span));
%         P_temp=fitlm((-span:span),c_temp);
%         P(j,:) = P_temp.Coefficients.Estimate;
%         if( mod(j,100)== 0)
%             plot(j/60, TT.Var1(j),'ko');
%             plot((j+(-span:span))/60, P(j,2)*(-span:span) + TT.Var1(j),'k');
%         end
%     end
%     
%     ACH = P(:,2)*-3600;
%     
%     del_t = 1:len_data;
%     idx = (del_t > (idx_start+timing_g(1,i))) & (del_t < (idx_start+timing_g(2,i)));
%     sum(idx)
%     figure(106);
%     subplot(3,4,i); hold on
%     plot(del_t/60,ACH);
%     plot(del_t(idx)/60,ACH(idx),'rx');
%     plot([idx_start+timing_g(1,i) idx_start+timing_g(1,i)]/60,[0 20],'k--');
%     plot([idx_start+timing_g(2,i) idx_start+timing_g(2,i)]/60,[0 20],'k--');
%     ylabel('ACH [1/h]');
% %     ylim([0,25]);
%     title(config);
%     ACH_mean_rms2(i,1) = mean(ACH(idx));
%     ACH_mean_rms2(i,2) = std(ACH(idx));


