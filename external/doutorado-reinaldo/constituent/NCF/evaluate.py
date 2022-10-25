import numpy as np
import torch


def hit(gt_item, pred_items):
	if gt_item in pred_items:
		return 1
	return 0


def ndcg(gt_item, pred_items):
	if gt_item in pred_items:
		index = pred_items.index(gt_item)
		return np.reciprocal(np.log2(index+2))
	return 0


def metrics(model, test_loader, top_k):
	HR, NDCG = [], []
	for user, item, label in test_loader:
		try:
			# user = user.cuda()
			user = user.cpu()
			# item = item.cuda()
			item = item.cpu()
			predictions = model(user, item)
			_, indices = torch.topk(predictions, top_k)
			recommends = torch.take(item, indices).cpu().numpy().tolist()
			gt_item = item[0].item()
			HR.append(hit(gt_item, recommends))
			NDCG.append(ndcg(gt_item, recommends))
		except:
			HR.append(0)
			NDCG.append(0)
	return np.mean(HR), np.mean(NDCG)
